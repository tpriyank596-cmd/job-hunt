# Browser techniques (tested on LinkedIn, Naukri, Indeed - Oct 2026)

Run these with `javascript_tool` (action `javascript_exec`). Top-level `await` works.

## 1. Capture hidden file inputs (no native file picker)

Many upload buttons create an `<input type=file>` on click and open the OS picker, which Claude cannot use. Patch `click` first (after every full page load), trigger the button from JS, then upload to the captured input.

```js
if(!HTMLInputElement.prototype.__origClick){
  HTMLInputElement.prototype.__origClick=HTMLInputElement.prototype.click;
  HTMLInputElement.prototype.click=function(){
    if(this.type==='file'){
      if(!this.isConnected){this.style.display='none';document.body.appendChild(this);}
      this.id='captured-resume-input';this.setAttribute('aria-label','Captured resume file input');
      window.__cap=this;return;}
    return this.__origClick();};
  HTMLInputElement.prototype.showPicker=function(){if(this.type==='file'){window.__cap=this;return;}};
}
```
Then: `[...document.querySelectorAll('button')].find(x=>/upload resume/i.test(x.innerText)).click()` → `find` "Captured resume file input" → `file_upload` with that ref. Wait 3 s and confirm the success toast and the file name.

If the page already has a real input (Naukri profile `#attachCV`), give it an aria-label and use `find` + `file_upload` directly.

Upload paths must be files this session may read: the session working directory and the uploads folder (where the user's attachments land) work; a copy placed only in an outputs folder was rejected once.

## 2. LinkedIn Easy Apply dialog helpers

The dialog is a plain div (not `[role=dialog]`). Define after opening Easy Apply:

```js
window.__dlg=()=>[...document.querySelectorAll('div')].filter(d=>/^Apply to /.test(d.innerText||'')).sort((a,b)=>a.innerText.length-b.innerText.length)[0];
window.__dump=()=>{const dlg=__dlg();if(!dlg)return 'no dialog';
  return [...dlg.querySelectorAll('input,select,textarea,button')].map((e,i)=>{
    const lab=(e.labels&&e.labels[0]?e.labels[0].innerText:'')||e.getAttribute('aria-label')||e.innerText||'';
    const v=e.tagName==='SELECT'?e.options[e.selectedIndex]?.text:(e.type==='radio'||e.type==='checkbox')?e.checked:e.value;
    return i+' '+e.tagName+':'+(e.type||'')+' | '+lab.replace(/\s+/g,' ').slice(0,110)+' | val='+v})
  .filter(s=>!(/radio/.test(s)&&/\.pdf|Document from/.test(s)&&/val=false/.test(s))).join('\n')
  +'\nPAGE:'+(dlg.innerText.match(/\d\/\d pages/)||[''])[0];};
window.__btn=(re)=>{const b=[...__dlg().querySelectorAll('button')].find(x=>re.test((x.innerText||'')+' '+(x.getAttribute('aria-label')||'')));if(b){b.click();return 'clicked'}return 'nobtn'};
window.__set=(i,val)=>{const e=[...__dlg().querySelectorAll('input,select,textarea,button')][i];
  const proto=e.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;
  Object.getOwnPropertyDescriptor(proto,'value').set.call(e,val);
  ['input','change','blur'].forEach(t=>e.dispatchEvent(new Event(t,{bubbles:true})));};
```
- Step forward: `__btn(/^\s*Next/)`, wait ~1.8 s, `__dump()`. Stop stepping when the dump shows text inputs, radios with questions, `Review` or `Submit application`.
- Radios: the label text is often not attached; on LinkedIn the order is Yes, No. Click by index and re-dump to confirm `checked`.
- Read the review block back: `__dlg().innerText` from "Additional Questions".
- Confirm success: `/application was sent|Application submitted/i.test(document.body.innerText)`.

## 3. Large reads without truncation

`javascript_tool` output truncates around ~1 KB. For big text, render it into the page and read it with `get_page_text` (≈50 KB):
```js
document.body.innerHTML='';const m=document.createElement('main');const p=document.createElement('pre');p.textContent=BIG_TEXT;m.appendChild(p);document.body.appendChild(m);
```
Only do this in a tab Claude opened and will navigate away from.

## 4. Long scripts

The JS call times out after ~45 s. Run long loops in the background (`(async()=>{...; window.__prog='DONE'})(); 'started'`) and poll `window.__prog`.

## 5. Naukri

- Job card fields on search pages: `.srp-jobtuple-wrapper[data-job-id]` → `.title`, `.comp-name`, `.expwdth`, `.sal-wrap`, `.locWdth`, `.tag-li`, `.job-post-day`, `a.title[href]`.
- Job page JD: `[class*="dang-inner-html"]`; header `[class*="jhc__"]`; stats `[class*="jhc__stat"]`; key skills `[class*="key-skill"] a`.
- Collect across pages in `localStorage` (same origin), then render once.
- Profile resume input: `#attachCV` on `https://www.naukri.com/mnjuser/profile`; current file name appears after the last "Resume\n" in body text.
- Apply button sits at the right of the job header card; confirmation URL contains `/myapply/saveApply` and text "Applied to".

## 6. LinkedIn search (logged-in UI hides job IDs)

Use the same-origin guest endpoints from a LinkedIn tab:
- List: `/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=..&location=..&f_TPR=r604800&start=0|10` → parse with regex on `data-entity-urn="urn:li:jobPosting:<id>"`, `base-search-card__title`, `base-search-card__subtitle`, `job-search-card__location`, `datetime="…"`. (`DOMParser` returned nothing here; use regex.) `f_WT=2` (remote) is ignored by this endpoint - verify mode from the JD.
- Detail: `/jobs-guest/jobs/api/jobPosting/<id>` → `show-more-less-html__markup` (JD), `description__job-criteria-text` (seniority, type), `num-applicants__caption`, "No longer accepting applications".
- Pace ~0.6-0.8 s between requests; ~60 list + ~70 detail requests per session was fine.
- Easy Apply vs external is not in guest data - check on the job page.

## 7. Indeed

- Search cards: `a[data-jk]` + `[data-testid=company-name]`, `[data-testid=text-location]`. Ignore obviously synthetic `jk` values (e.g. `abcdef0123456789`, `fedcba9876543210`) - they were duplicate placeholders.
- Job page text: body between "Full job description" and "Is there a problem".
- Cloudflare challenge pages appear intermittently; never retry in a loop.
