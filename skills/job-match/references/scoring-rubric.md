# Scoring rubric

Total 100 points. Round to the nearest whole number.

## 1. Must-have skills (35)

`35 × (matched must-haves ÷ total must-haves)`, where:
- Primary skill match = 1.0
- Secondary skill match = 0.5
- Close synonym / same family = 0.75 (e.g. job wants Flask, user has FastAPI + Django)
- Stated in chat but not on resume = 0.75 (and flag "add to resume")
- No match = 0

If the JD has no clear technical requirements (very short JD), give 20 and set confidence low.

## 2. Experience fit (20)

Let `req_min`, `req_max` be the JD range, `exp` the relevant experience.

| Situation | Points |
| --- | --- |
| `req_min ≤ exp ≤ req_max` | 20 |
| `exp` within 1 year below `req_min` | 14 |
| 1-2 years below | 8 |
| 3+ years below | 0 and hard knockout |
| Above `req_max` by ≤3 years | 16 |
| Above `req_max` by more than 3 years | 10 (flag overqualified) |
| Not specified | 15, confidence medium |

## 3. Role / title fit (15)

| Situation | Points |
| --- | --- |
| Same role family and level as a target role | 15 |
| Same family, one level off (e.g. Senior vs mid) | 10 |
| Adjacent family (e.g. Backend → Full-stack, ML Eng → Data Eng) | 8 |
| Unrelated (e.g. Backend → QA Manual) | 0 |

## 4. Location & work mode (10)

| Situation | Points |
| --- | --- |
| In a target city with the preferred mode, or remote when remote is wanted | 10 |
| Target city but different mode (e.g. on-site when hybrid preferred) | 6 |
| Other city, user open to relocation | 5 |
| Other city, user not open to relocation, not remote | 0 and hard knockout |

## 5. Nice-to-have skills (10)

`10 × (matched nice-to-haves ÷ total nice-to-haves)`, same match weights as must-haves. No nice-to-haves listed → 7.

## 6. CTC fit (5)

| Situation | Points |
| --- | --- |
| Range overlaps expected CTC | 5 |
| Not disclosed | 3 |
| Below expected but above current | 2 |
| Below current | 0 and flag |

## 7. Other signals (5)

Start at 5 and subtract:
- −3 notice period conflict ("immediate joiners" vs 60-90 days)
- −2 education requirement not met (and not "or equivalent experience")
- −1 domain mismatch the JD calls mandatory (e.g. "fintech experience required")
Minimum 0.

## Confidence

- **High:** full JD, clear requirements, experience range given.
- **Medium:** one of the above missing.
- **Low:** partial JD (login wall), very short JD, or mostly boilerplate.

## Common synonym families

- Python web: Django, Flask, FastAPI
- JS front-end: React, Next.js; Vue, Nuxt; Angular
- Node back-end: Node.js, Express, NestJS
- Java: Spring, Spring Boot
- Cloud: AWS, GCP, Azure (count as 0.5 for each other unless JD names one as mandatory)
- Queues/streams: SQS, RabbitMQ, Kafka, Pub/Sub, Celery (0.75 within the family)
- SQL DBs: PostgreSQL, MySQL, SQL Server
- NoSQL: MongoDB, DynamoDB, Cassandra, Redis (Redis only as cache/KV)
- Vector DBs: Pinecone, Weaviate, Qdrant, Milvus, pgvector, FAISS
- LLM frameworks: LangChain, LangGraph, LlamaIndex, Semantic Kernel, CrewAI
- Containers: Docker, Kubernetes (Docker alone counts 0.5 for a Kubernetes requirement)
- Realtime: WebSockets, Socket.IO
