# Structured Literature Search — Protocol (A17)

**Fixed 3 November 2026, and committed before any query.** The commit that adds this file is the protocol's date of record. It is the literature counterpart of the evaluation freeze: what is searched, how, and what counts as a threat to the novelty claim are fixed here, before any result exists.

- **Category:** 01, Research. **Tier:** 💾 Offline: kept in the repository and on your computer, not in Project Knowledge.
- **Builds on:** the novelty claim (D7, with A28's draft wording), `sources.md`, and `00-action-items.md` A17, A28, A29, A33 and A42.
- **Feeds:** one `sources.md` entry per run, the Literature Review chapter and its search appendix, and A28's opening clause.
- **Decided by:** the user on 2 November 2026 (D32, D34), on the independent A17 review of 30 October 2026: its option (e), packaged with option (d).
- **Changing it:** any change after the first query is logged in `sources.md` with both versions and the reason, before the runs it affects are reported. Nothing else here changes.

## 1. What this is, and what it is not

It is a **structured, documented search**: fixed strings, run in named indexes on recorded dates, with every count recorded so anyone can re-run it. It is **not a systematic review** in the PRISMA sense, and the thesis never calls it one.

Thirteen iterations of broad web searching found the nearest work, but none of them recorded strings or counts that can be re-run. One known paper was missed by keyword search and caught only by citation chasing: TrapManager (#326), found because it cites #323 (#327). So this protocol pairs keyword strings with forward-citation searches.

## 2. Who runs it, and how

**The queries run from your browser.** Claude's environment could not reach any index on 30 October 2026: every query was refused, and no count came back (#402, verified). OpenAlex and Semantic Scholar need no key (#397, #398).

Each query below is a web address that returns JSON:
- For OpenAlex, the count is `meta` → `count`.
- For Semantic Scholar, it is `total`, which that index calls an estimate.

Send Claude the counts, or the saved JSON. Keep the raw JSON files on your computer (💾). If a Claude chat fetches one of these addresses for you, check its count against the raw JSON, because that tool summarises pages.

## 3. The indexes and their roles

| Role | Index |
|---|---|
| Principal, counted | OpenAlex (`search.title_and_abstract`) and Semantic Scholar (bulk search) |
| Recency check | arXiv: strings S1 and S2 |
| Conditional | IEEE Xplore's public search: S1 and S4, if it is usable from your browser. If it is not, the thesis limitation names it |
| Forward citations | OpenAlex `cites:` and Google Scholar's "Cited by" |
| Not used for keyword search | Crossref: DOI and metadata lookup only, because its keyword search is not documented as boolean (#400) |
| Not used for counts | Google Scholar keyword search: its "about N results" cannot be re-run (#395) |
| TechRxiv | Through OpenAlex. Check by looking up #372's DOI there. If it is missing, run S1 on TechRxiv's own site |
| Patents | Google Patents and the USPTO's Patent Public Search (§8) |

## 4. The strings

**Concept blocks,** matched on title and abstract:
- **D, deception:** `honeypot OR honeynet OR honeytoken OR decoy OR "cyber deception" OR "defensive deception" OR "deception technology" OR "deceptive defense"`. Bare "deception" is left out, because control theory uses "deception attack" for false-data injection.
- **P, placement:** `placement OR allocation OR deployment OR selection OR positioning`
- **O, OT:** `"industrial control" OR SCADA OR ICS OR "operational technology" OR "cyber-physical" OR "programmable logic controller" OR "smart grid" OR substation OR "critical infrastructure" OR IIoT`. PLC is spelled out, because the abbreviation also means phospholipase C.
- **Z, zones:** `"62443" OR "zones and conduits" OR "zone and conduit" OR Purdue`
- **M, method:** `optimization OR optimisation OR optimal OR "integer programming" OR MILP OR submodular OR greedy OR game OR Stackelberg OR "reinforcement learning"`
- **A, attack paths:** `"attack path" OR "attack graph" OR MITRE OR "kill chain" OR "lateral movement"`

**The five strings:**
- **S1** = D AND P AND O
- **S2** = D AND M AND O
- **S3** = D AND Z
- **S4** = `(placement OR allocation OR optimization OR optimisation OR "integer programming") AND ("62443" OR "zones and conduits" OR "zone and conduit")`. This is the "what would break it" test from `03-honest-review.md` §B, with no deception term.
- **S5** = D AND A AND O

**Limits:** all years up to the search date; all record types, theses and reports included; records with an English title or abstract.

## 5. The pilot (about five minutes): ten counts

Open each address, and record its count, the date and the time.

**OpenAlex** (count: `meta.count`):
```
S1  https://api.openalex.org/works?search.title_and_abstract=(honeypot OR honeynet OR honeytoken OR decoy OR "cyber deception" OR "defensive deception" OR "deception technology" OR "deceptive defense") AND (placement OR allocation OR deployment OR selection OR positioning) AND ("industrial control" OR SCADA OR ICS OR "operational technology" OR "cyber-physical" OR "programmable logic controller" OR "smart grid" OR substation OR "critical infrastructure" OR IIoT)&per_page=200&select=id,doi,display_name,publication_year

S2  https://api.openalex.org/works?search.title_and_abstract=(honeypot OR honeynet OR honeytoken OR decoy OR "cyber deception" OR "defensive deception" OR "deception technology" OR "deceptive defense") AND (optimization OR optimisation OR optimal OR "integer programming" OR MILP OR submodular OR greedy OR game OR Stackelberg OR "reinforcement learning") AND ("industrial control" OR SCADA OR ICS OR "operational technology" OR "cyber-physical" OR "programmable logic controller" OR "smart grid" OR substation OR "critical infrastructure" OR IIoT)&per_page=200&select=id,doi,display_name,publication_year

S3  https://api.openalex.org/works?search.title_and_abstract=(honeypot OR honeynet OR honeytoken OR decoy OR "cyber deception" OR "defensive deception" OR "deception technology" OR "deceptive defense") AND ("62443" OR "zones and conduits" OR "zone and conduit" OR Purdue)&per_page=200&select=id,doi,display_name,publication_year

S4  https://api.openalex.org/works?search.title_and_abstract=(placement OR allocation OR optimization OR optimisation OR "integer programming") AND ("62443" OR "zones and conduits" OR "zone and conduit")&per_page=200&select=id,doi,display_name,publication_year

S5  https://api.openalex.org/works?search.title_and_abstract=(honeypot OR honeynet OR honeytoken OR decoy OR "cyber deception" OR "defensive deception" OR "deception technology" OR "deceptive defense") AND ("attack path" OR "attack graph" OR MITRE OR "kill chain" OR "lateral movement") AND ("industrial control" OR SCADA OR ICS OR "operational technology" OR "cyber-physical" OR "programmable logic controller" OR "smart grid" OR substation OR "critical infrastructure" OR IIoT)&per_page=200&select=id,doi,display_name,publication_year
```

**Semantic Scholar** (count: `total`). Here `|` is OR, and `%2B` is a literal `+`, which is AND. "cyber physical" is written without its hyphen, in case the hyphen is read as NOT.
```
S1  https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=(honeypot | honeynet | honeytoken | decoy | "cyber deception" | "defensive deception" | "deception technology" | "deceptive defense") %2B (placement | allocation | deployment | selection | positioning) %2B ("industrial control" | SCADA | ICS | "operational technology" | "cyber physical" | "programmable logic controller" | "smart grid" | substation | "critical infrastructure" | IIoT)&fields=title,year,externalIds,venue

S2  https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=(honeypot | honeynet | honeytoken | decoy | "cyber deception" | "defensive deception" | "deception technology" | "deceptive defense") %2B (optimization | optimisation | optimal | "integer programming" | MILP | submodular | greedy | game | Stackelberg | "reinforcement learning") %2B ("industrial control" | SCADA | ICS | "operational technology" | "cyber physical" | "programmable logic controller" | "smart grid" | substation | "critical infrastructure" | IIoT)&fields=title,year,externalIds,venue

S3  https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=(honeypot | honeynet | honeytoken | decoy | "cyber deception" | "defensive deception" | "deception technology" | "deceptive defense") %2B ("62443" | "zones and conduits" | "zone and conduit" | Purdue)&fields=title,year,externalIds,venue

S4  https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=(placement | allocation | optimization | optimisation | "integer programming") %2B ("62443" | "zones and conduits" | "zone and conduit")&fields=title,year,externalIds,venue

S5  https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=(honeypot | honeynet | honeytoken | decoy | "cyber deception" | "defensive deception" | "deception technology" | "deceptive defense") %2B ("attack path" | "attack graph" | MITRE | "kill chain" | "lateral movement") %2B ("industrial control" | SCADA | ICS | "operational technology" | "cyber physical" | "programmable logic controller" | "smart grid" | substation | "critical infrastructure" | IIoT)&fields=title,year,externalIds,venue
```

These addresses follow each index's documented syntax (#397, #398). Whether each runs as written is unconfirmed, and the pilot is its test. If one returns an error, it is amended once and both versions are recorded. A "429 too many requests" reply from Semantic Scholar means wait a minute and retry, and it is not a result.

**What the pilot decides:**
- *Over about 3,000 unique records in total:* tighten the strings under the stopping rule (§6) before screening.
- *Under about 30:* the search is cheaper than estimated.
- *Either way:* the counts are recorded as the first runs.

## 6. Checks fixed in advance

- **Known-item test, before any screening.** S1 should retrieve Jay (#305) and Mashima (#12); check DecIED (#11) as well. If any is missing, diagnose why, amend the strings once, and record both versions.
- **Stopping rule.** A string that returns more than 1,500 records in one index is narrowed once before screening, and both runs are recorded.
- **Self-hits.** This project's own repository and documents are removed from every result list.

## 7. Forward citations: eight anchor papers

| Anchor | Identifier | OpenAlex lookup |
|---|---|---|
| Jay 2023, #305 | doi:10.1109/ACCESS.2023.3279504 | `https://api.openalex.org/works/doi:10.1109/ACCESS.2023.3279504` |
| Zambianco et al., #24 | arXiv 2404.12783 | `https://api.openalex.org/works/doi:10.48550/arXiv.2404.12783` |
| Zambianco et al., #25 | arXiv 2303.03151 | `https://api.openalex.org/works/doi:10.48550/arXiv.2303.03151` |
| Osman et al., #323 | doi:10.1145/3630049.3630169 | `https://api.openalex.org/works/doi:10.1145/3630049.3630169` |
| Kulkarni et al., #236 | arXiv 2407.14436 | `https://api.openalex.org/works/doi:10.48550/arXiv.2407.14436` |
| TrapManager, #326 | doi:10.3390/math14040683 | `https://api.openalex.org/works/doi:10.3390/math14040683` |
| Valeros et al., #40 | arXiv 2606.27966 | `https://api.openalex.org/works/doi:10.48550/arXiv.2606.27966` |
| The IEC 62443 attack-path paper, #269 | title only | `https://api.openalex.org/works?search=cybersecurity risk assessment methodology industrial automation control systems&select=id,doi,display_name,publication_year` |

For each anchor:
1. Take its OpenAlex id (`W…`) from the lookup. For a published paper that also has an arXiv preprint, use both records.
2. List the papers citing it: `https://api.openalex.org/works?filter=cites:W…&per_page=200&select=id,doi,display_name,publication_year`.
3. Open its Google Scholar "Cited by" list as well.
4. Give any new close match one backward round and one forward round.
5. Stop after two rounds, or earlier if a round adds nothing close.

## 8. The patent arm (A29)

- S1 as a Google Patents search.
- Assignee searches: Acalvio, TrapX/Commvault, Attivo/SentinelOne, Illusive/Proofpoint, Fortinet and CounterCraft.
- The classification group H04L 63/1491. Its title is unverified, so the first run records what the group covers.
- The patents citing US 9,853,999 (#347).
- The leads in #374 and #390, and US 10,291,650 (#401).

Screen each patent on its title, abstract and first independent claim. Read the full claims of any patent that selects positions.

## 9. Screening

1. **Deduplicate,** by DOI, then by normalised title and year, merging preprints with their published versions. Record the counts before and after.
2. **Remove self-hits.**
3. **Screen titles inclusively, then abstracts.**
4. **Sort what remains into tiers:**
   - **T3, threatens the claim:** selects deception positions in a multi-zone OT/ICS network by optimising a stated objective, with zone or conduit structure and criticality as numeric inputs.
   - **T2, narrows the claim:** formal deception-placement optimisation in OT, ICS or CPS that lacks one of those elements; or any placement optimisation that uses IEC 62443 zones as a numeric input.
   - **T1, related:** cited as needed.
5. **Exclude:** non-cyber senses of the terms; vendor pages, which `03-commercial-prior-art-analysis.md` already covers; duplicates.

An AI first pass may sort titles. You confirm every T2 and T3 decision, and every exclusion of a title that carries both a deception term and an OT term.

## 10. Recording

Recording follows PRISMA-S (#394) items 1, 5, 8, 9, 13, 15 and 16.
- **One numbered `sources.md` entry per run,** giving:
  - the index and endpoint;
  - the string exactly as run;
  - the limits, the date and the count (Semantic Scholar's marked as an estimate);
  - the number of new records after deduplication;
  - the outcome at each screening stage;
  - how many records became new entries and how many were already logged.
- **A run that keeps nothing** is titled "Negative result", with its string, date and count.
- **Each kept record** gets its own entry, with a verification marker.
- **An update re-run** of S1 and the citation lists is made within a month of submission (PRISMA-S item 12).

## 11. If a T2 or T3 work turns up

1. Do not judge it from its abstract. Iteration 13 and D22 both went wrong that way.
2. Get the full text: an open copy, an email to the author, or a PDF you supply.
3. Map it clause by clause against D7 and A28, as `03-commercial-prior-art-analysis.md` §4 does.
4. Log it in `sources.md` with a marker.
5. Write a decisions-log entry stating its effect on the claim, favourable or not.
6. If this happens before the freeze, decide whether it becomes a baseline.
7. If it is T3, narrow A28 to the distinction that survives.

## 12. Timing and effort

The literature part runs **before A12 and the freeze**, so that a competing method it finds can still become a baseline. Found after Phase D, such a method could only be reported as a limitation.

| Task | Estimate |
|---|---|
| Queries | 2–3 hours |
| Deduplication | 1 hour |
| Screening an estimated 300–800 records | 3–6 hours |
| Reading 0–3 full texts | up to 4 hours |
| **Literature part, in total** | **about 1 weekend-unit** |
| Patents | +0.5–1 weekend-units |
| Write-up | +0.25 |
| Update re-run | +0.1–0.2 |

The volumes are unmeasured until the pilot runs.

## 13. What the thesis says

**The limitation, worded in advance** (the brackets are filled from the runs):

> The literature review is not a systematic review in the PRISMA sense. It combined thirteen rounds of broad, multi-angle web searching ([period]), recorded in a source log but not reproducible query by query, with a structured search fixed in advance and run on [date]: five search strings in two open scholarly indexes, OpenAlex and Semantic Scholar, with a recency check on arXiv[, and in IEEE Xplore's public search interface]; forward-citation searches on eight anchor papers through OpenAlex and Google Scholar; and a patent search in Google Patents and the USPTO's Patent Public Search. Appendix [X] lists every string exactly as run, with its date and record count. The subscription databases Scopus and Web of Science were not searched, because no institutional access was available. Open indexes lack abstracts for some publishers, so some records could be matched on title alone; one reviewer screened the records; and only records with an English title or abstract were screened. A relevant work indexed only in subscription databases, or described in vocabulary none of the strings anticipated and citing none of the anchor papers, could have been missed. The novelty claim is stated to the best of this search.

**A28's opening clause, once the search and A29's patent sweep have run:** "To the best of a documented search of open scholarly indexes and granted patents, …".

**Two works not to cite until read in full:** Gusenbauer & Haddaway (#395) and Wohlin (#396).
