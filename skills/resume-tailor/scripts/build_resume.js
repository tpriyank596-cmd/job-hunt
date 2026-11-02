// Build ATS-safe single-column DOCX resumes from a facts file.
// Usage: node build_resume.js <facts.json> <outDir> [variantKey|all] [maxBulletsRole1,maxBulletsRole2,...] [maxProjects]
// facts.json holds ONLY true facts from the user's resume; variants only choose order, wording keys and summary/skills text.
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, BorderStyle, TabStopType } = require('docx');

const [factsPath, outDir, which = 'all', limitsArg = '', projArg = ''] = process.argv.slice(2);
if (!factsPath || !outDir) { console.error('usage: node build_resume.js facts.json outDir [variant|all] [6,4] [2]'); process.exit(1); }
const F = JSON.parse(fs.readFileSync(factsPath, 'utf8'));
const limits = limitsArg ? limitsArg.split(',').map(Number) : (F.limits?.bullets || []);
const maxProjects = projArg ? Number(projArg) : (F.limits?.projects ?? 99);
const font = F.style?.font || 'Calibri';
const size = F.style?.size || 19; // half-points
const t = (text, o = {}) => new TextRun({ text, font, size: o.size || size, bold: o.bold, italics: o.italics });
const heading = s => new Paragraph({ spacing: { before: 140, after: 50 }, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: '444444', space: 1 } }, children: [t(s.toUpperCase(), { bold: true, size: size + 3 })] });
const bullet = s => new Paragraph({ numbering: { reference: 'b', level: 0 }, spacing: { after: 20 }, children: [t(s)] });
const roleLine = (l, r) => new Paragraph({ tabStops: [{ type: TabStopType.RIGHT, position: 10466 }], spacing: { before: 60, after: 20 }, children: [t(l, { bold: true }), t('\t' + r, { bold: true })] });
const sub = s => new Paragraph({ spacing: { after: 20 }, children: [t(s, { italics: true })] });

function build(key) {
  const v = F.variants[key];
  if (!v) throw new Error('unknown variant ' + key);
  const kids = [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 20 }, children: [t(F.name, { bold: true, size: size + 11 })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [t(F.contact)] }),
    heading('Summary'), new Paragraph({ spacing: { after: 20 }, children: [t(v.summary)] }),
    heading('Skills'),
    ...v.skills.map(([k, s]) => new Paragraph({ spacing: { after: 20 }, children: [t(k + ': ', { bold: true }), t(s)] })),
    heading('Experience'),
  ];
  F.experience.forEach((role, i) => {
    kids.push(roleLine(`${role.title} | ${role.company}`, role.dates));
    if (role.subtitle) kids.push(sub(role.subtitle));
    const order = (v.order && v.order[i]) || Object.keys(role.bullets);
    const lim = limits[i] ?? order.length;
    order.slice(0, lim).forEach(k => { if (!role.bullets[k]) throw new Error(`missing bullet ${k} in role ${i}`); kids.push(bullet(role.bullets[k])); });
  });
  const projKeys = (v.projects || Object.keys(F.projects || {})).slice(0, maxProjects);
  if (projKeys.length) {
    kids.push(heading('Projects'));
    projKeys.forEach(k => { const [n, s, bs] = F.projects[k]; kids.push(new Paragraph({ spacing: { before: 50, after: 20 }, children: [t(n, { bold: true }), t(' — ' + s, { italics: true })] }), ...bs.map(bullet)); });
  }
  kids.push(heading('Education'));
  F.education.forEach(e => { kids.push(roleLine(e.line, e.dates)); if (e.sub) kids.push(sub(e.sub)); });
  if (F.certifications) { kids.push(heading('Certifications'), new Paragraph({ children: [t(F.certifications)] })); }
  const doc = new Document({
    numbering: { config: [{ reference: 'b', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 300, hanging: 220 } } } }] }] },
    sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 480, bottom: 440, left: 680, right: 680 } } }, children: kids }],
  });
  return Packer.toBuffer(doc).then(b => { const f = path.join(outDir, v.file + '.docx'); fs.writeFileSync(f, b); return f; });
}
fs.mkdirSync(outDir, { recursive: true });
const keys = which === 'all' ? Object.keys(F.variants) : which.split(',');
Promise.all(keys.map(build)).then(f => console.log(f.join('\n'))).catch(e => { console.error(e.message); process.exit(1); });
