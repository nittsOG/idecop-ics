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
| Patents | Google Patents (§8; amendment 5) |

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

*Amended 14 November 2026 (amendment 3): the term "honeypoint".* *Before:* block D had no word for a decoy called a "honeypoint", which one group of authors uses. *After:* the five strings are unchanged, and two further runs search the term alone: OpenAlex `search.title_and_abstract=(honeypoint OR honeypoints)` and the same query on Google Patents (`sources.md` #618, #626). *Why:* BAG-HRF (record 419 of `01-search-screening-record.md`), titled with the word, was first found by this run; none of the five strings returned it. Old and new wording, and the reason, are in `sources.md` #643.

*A gap in block O, found 15 November 2026 (stated with amendment 7; the strings are unchanged).* Block O has "smart grid" and "substation" but no word for a power network: "power grid", "power system", "electric power", "new power system", "distribution network" and "power plant" are missing. S1, S2 and S5 use the block on the paper side, and S1 (runs P1 and P1n) and the classification run P3b use it on the patent side, so a work that describes a power network in those words and carries no other word of the block is not returned by them. S3, S4, P1b, the assignee, citation and lead runs and P6 do not use it, and neither do the earlier rounds of web searching or the forward-citation searches (§7); how much those routes covered was not measured. The text of CN 121356815 A, as read, has no word of the block. The gap is described in `01-search-screening-record.md` §14.5; a widened re-run is offered in D36 and has not been made. *D38: made on 16 November 2026 and screened (amendment 8, below); one paper that narrows the claim, Zhan et al. 2026, was returned only through the new words (`01-search-screening-record.md` §18).*

*Amended 16 November 2026 (amendment 8; approved by the user in D37, run and recorded in D38): the widened re-run of block O.* *Before:* the five strings used block O alone, and the gap above was stated and left. *After:* block O′, `"power grid" OR "power system" OR "electric power" OR "new power system" OR "distribution network" OR "power plant"`, is run once in place of block O: S1, S2 and S5 on OpenAlex and Semantic Scholar (runs R1–R6) and S1 on Google Patents, narrowed as P1n was (run P1c, §8). Records the first runs returned are dropped. The five strings and block O are unchanged; the classification run P3b was not repeated. *Why:* D36 item 6. *Logged:* `sources.md` #990, with the runs after it (#991–#997).

## 5. The pilot (about five minutes): ten counts

Open each address, and record its count, the date and the time. Copy only the address itself, from `https` onward: a label copied with it makes the browser search for the text instead of opening it.

**OpenAlex** (count: `meta.count`):

S1
```
https://api.openalex.org/works?search.title_and_abstract=(honeypot OR honeynet OR honeytoken OR decoy OR "cyber deception" OR "defensive deception" OR "deception technology" OR "deceptive defense") AND (placement OR allocation OR deployment OR selection OR positioning) AND ("industrial control" OR SCADA OR ICS OR "operational technology" OR "cyber-physical" OR "programmable logic controller" OR "smart grid" OR substation OR "critical infrastructure" OR IIoT)&per_page=200&select=id,doi,display_name,publication_year
```

S2
```
https://api.openalex.org/works?search.title_and_abstract=(honeypot OR honeynet OR honeytoken OR decoy OR "cyber deception" OR "defensive deception" OR "deception technology" OR "deceptive defense") AND (optimization OR optimisation OR optimal OR "integer programming" OR MILP OR submodular OR greedy OR game OR Stackelberg OR "reinforcement learning") AND ("industrial control" OR SCADA OR ICS OR "operational technology" OR "cyber-physical" OR "programmable logic controller" OR "smart grid" OR substation OR "critical infrastructure" OR IIoT)&per_page=200&select=id,doi,display_name,publication_year
```

S3
```
https://api.openalex.org/works?search.title_and_abstract=(honeypot OR honeynet OR honeytoken OR decoy OR "cyber deception" OR "defensive deception" OR "deception technology" OR "deceptive defense") AND ("62443" OR "zones and conduits" OR "zone and conduit" OR Purdue)&per_page=200&select=id,doi,display_name,publication_year
```

S4
```
https://api.openalex.org/works?search.title_and_abstract=(placement OR allocation OR optimization OR optimisation OR "integer programming") AND ("62443" OR "zones and conduits" OR "zone and conduit")&per_page=200&select=id,doi,display_name,publication_year
```

S5
```
https://api.openalex.org/works?search.title_and_abstract=(honeypot OR honeynet OR honeytoken OR decoy OR "cyber deception" OR "defensive deception" OR "deception technology" OR "deceptive defense") AND ("attack path" OR "attack graph" OR MITRE OR "kill chain" OR "lateral movement") AND ("industrial control" OR SCADA OR ICS OR "operational technology" OR "cyber-physical" OR "programmable logic controller" OR "smart grid" OR substation OR "critical infrastructure" OR IIoT)&per_page=200&select=id,doi,display_name,publication_year
```

**Semantic Scholar** (count: `total`). Its bulk search refuses the characters `(` `)` `|` `"` written raw (HTTP 400), so they are written encoded: `%28` and `%29` for brackets, `%7C` for OR, `%22` for a quote mark, and `%2B` for AND. "cyber physical" is written without its hyphen, in case the hyphen is read as NOT.

S1
```
https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=%28honeypot %7C honeynet %7C honeytoken %7C decoy %7C %22cyber deception%22 %7C %22defensive deception%22 %7C %22deception technology%22 %7C %22deceptive defense%22%29 %2B %28placement %7C allocation %7C deployment %7C selection %7C positioning%29 %2B %28%22industrial control%22 %7C SCADA %7C ICS %7C %22operational technology%22 %7C %22cyber physical%22 %7C %22programmable logic controller%22 %7C %22smart grid%22 %7C substation %7C %22critical infrastructure%22 %7C IIoT%29&fields=title,year,externalIds,venue
```

S2
```
https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=%28honeypot %7C honeynet %7C honeytoken %7C decoy %7C %22cyber deception%22 %7C %22defensive deception%22 %7C %22deception technology%22 %7C %22deceptive defense%22%29 %2B %28optimization %7C optimisation %7C optimal %7C %22integer programming%22 %7C MILP %7C submodular %7C greedy %7C game %7C Stackelberg %7C %22reinforcement learning%22%29 %2B %28%22industrial control%22 %7C SCADA %7C ICS %7C %22operational technology%22 %7C %22cyber physical%22 %7C %22programmable logic controller%22 %7C %22smart grid%22 %7C substation %7C %22critical infrastructure%22 %7C IIoT%29&fields=title,year,externalIds,venue
```

S3
```
https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=%28honeypot %7C honeynet %7C honeytoken %7C decoy %7C %22cyber deception%22 %7C %22defensive deception%22 %7C %22deception technology%22 %7C %22deceptive defense%22%29 %2B %28%2262443%22 %7C %22zones and conduits%22 %7C %22zone and conduit%22 %7C Purdue%29&fields=title,year,externalIds,venue
```

S4
```
https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=%28placement %7C allocation %7C optimization %7C optimisation %7C %22integer programming%22%29 %2B %28%2262443%22 %7C %22zones and conduits%22 %7C %22zone and conduit%22%29&fields=title,year,externalIds,venue
```

S5
```
https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=%28honeypot %7C honeynet %7C honeytoken %7C decoy %7C %22cyber deception%22 %7C %22defensive deception%22 %7C %22deception technology%22 %7C %22deceptive defense%22%29 %2B %28%22attack path%22 %7C %22attack graph%22 %7C MITRE %7C %22kill chain%22 %7C %22lateral movement%22%29 %2B %28%22industrial control%22 %7C SCADA %7C ICS %7C %22operational technology%22 %7C %22cyber physical%22 %7C %22programmable logic controller%22 %7C %22smart grid%22 %7C substation %7C %22critical infrastructure%22 %7C IIoT%29&fields=title,year,externalIds,venue
```

*Amended 5 November 2026: the protocol's one amendment.* OpenAlex ran as written. Semantic Scholar refused the first form of all five strings with HTTP 400, and diagnostic tests showed that it accepts the same characters encoded (`sources.md` #410). So the Semantic Scholar strings above are the first form with `(` `)` `|` `"` encoded, and their logic is unchanged. The first form, the tests and every count are in `sources.md` #405–#416. The labels S1–S5 now sit outside the code blocks.

A "429 too many requests" reply from Semantic Scholar means wait a minute and retry. It is not a result.

**What the pilot decides:**
- *Over about 3,000 unique records in total:* tighten the strings under the stopping rule (§6) before screening.
- *Under about 30:* the search is cheaper than estimated.
- *Either way:* the counts are recorded as the first runs.

*Result, 5 November 2026:* 758 records, 375 unique after deduplication. That is under both thresholds, so no string was narrowed (`sources.md` #416).

## 6. Checks fixed in advance

- **Known-item test, before any screening.** S1 should retrieve Jay (#305) and Mashima (#12); check DecIED (#11) as well. If any is missing, diagnose why, amend the strings once, and record both versions. *Passed, 4–5 November 2026: S1 retrieved all three in both indexes (`sources.md` #405, #411).*
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
- *Added 15 November 2026 (amendment 7):* the similarity route, run P6 (`sources.md` #640). From the Google Patents page of each of the closest patents found, the patents and papers named in its "Similar documents", "Patent citations", "Cited by" and "Families citing this family" tables: nine pages (level 1) and the seven pages that level 1 led to (level 2), then stop.
- *Added 16 November 2026 (amendment 8):* run P1c, S1 with block O′ in place of block O (§4), narrowed to title, abstract and claims as P1n was (`sources.md` #997).

Screen each patent on its title, abstract and first independent claim. Read the full claims of any patent that selects positions.

*Result, 14–15 November 2026:* S1 on Google Patents' full text returned about 24,680, over §6's limit of 1,500, so it was narrowed once, to its title, abstract and claims (about 260; `sources.md` #624, #625); this is §6 applied, not an amendment. The assignee, classification, citation and lead runs followed (#627–#639), and then the similarity route (P6, #640; amendment 7). The arm surfaced 1,394 distinct publication numbers: T3 0; T2 1, proposed; related (T1) 712; excluded 681 *[D37: T2 2, both confirmed by the user, and related (T1) 711; CN 121012683 A moved from T1]*. No patent threatens A28's claim as worded (`sources.md` #642; D36). *[D38: run P1c (amendment 8) adds 102 publication numbers: related (T1) 32, excluded 70; the arm counts 1,496: T2 2, related (T1) 743, excluded 751 (`01-search-screening-record.md` §18.4).]*

*Amended 15 November 2026 (amendment 6): how patents were screened.* *Before:* "Screen each patent on its title, abstract and first independent claim." *After:* patents were screened on their titles by a keyword rule (`01-search-screening-record.md` §14.2). The page of a patent whose title suggested placement or deployment, of every lead above and of the nearest of the patents citing #347 was opened and read (91 pages). Because every result of the narrowed S1 carries a deception word, a placement word and an OT word in its title, abstract or claims, four more rounds followed: a second (41; run P1n), a third (68; candidates of runs P1n, P3b and P1b whose titles suggested a strategy, a game or an attack path, and security titles that the rule had excluded), a fourth (39; a last check of excluded titles that named a security, attack or defence topic or that Google Patents had cut) and a fifth (23; patents named by the similarity route of amendment 7). 262 pages were opened in all, and 1,128 patents were judged on a title alone. *Why:* 1,394 patents are far more than one reviewer can take through three fields each, and the protocol gave no volume for the patent arm (§12 estimated only the papers). *Cost, stated openly:* a placement method behind a neutral title could have been missed, and the rule's exclusions are not safe: of the 29 excluded titles opened in the third round, 19 proved related (T1) on reading and 10 stayed excluded; of the 39 opened in the fourth, 26 proved related and 13 stayed excluded. The rule was written during the screening, not before it. *Added by Claude beyond the amendments the user approved; the user can strike it.* *[D37: kept by the user, 16 November 2026.]*

*Amended 15 November 2026 (amendment 7): a route that starts from a patent.* *Before:* §8 listed runs P1 to P5 and gave no route that starts from a patent. *After:* §8 adds run P6 (above): the tables on the Google Patents pages of nine of the closest patents and of seven pages that those led to. The 243 patent rows (229 distinct patents) were screened on their titles by the rule of amendment 6; of the 60 with a deception term in the title, 27 were in the data already (45 per cent) and 33 were new; 38 patents are new to the data (20 opened and 18 judged on a title alone), 71 patents carry the run, and none is T2 or T3. The 193 paper rows on the same pages were typed by title (`sources.md` #641). *Why:* CN 121356815 A (#771), a placement method with a stated objective behind a cut title and a text with no OT word, showed that the keyword runs can miss a neighbour; the tables are Google's own similarity and citation links and do not depend on our query words. *Cost, stated openly:* the depth of two and the choice of the sixteen pages are Claude's, and the route was not run to saturation; the tables of seven formal placement patents read at level 1 were not taken; 158 rows with no deception term in the title were counted and not entered; a table shows what Google chooses to show; and the pages were read through a fetch tool that returns a summary, so a row can be wrong. *Added by Claude beyond the amendments the user approved; the user can strike it.* *[D37: kept by the user, 16 November 2026.]*

*Amended 15 November 2026 (amendment 5, a correction):* §3's table row and §13's limitation said patents were searched in "Google Patents and the USPTO's Patent Public Search". §8 specified Google Patents only, and no search on the USPTO's own site was run; both places now say Google Patents only. Google Patents covers US grants and applications and EP, WO, CN, KR and JP documents.

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
  *Amended 15 November 2026 (amendment 4, the user's decision, option (a)): how patents are recorded.* *Before:* every kept record had its own entry; patents were not distinguished. *After:* papers follow this section as written; for patents, an entry for every run and one for every patent whose page was opened (262); the other patents appear only in the screening record's tables (`01-search-screening-record.md` §14–§17), with their runs and tiers. *Why:* 1,394 publication numbers, 1,128 of them judged on a title alone, would have added about 1,128 entries to a log of 612 and buried the 262 that were read. *Cost, stated openly:* the two arms are recorded differently; nothing is lost, since every number, run and tier is in the record.
- **An update re-run** of S1 and the citation lists is made within a month of submission (PRISMA-S item 12).

## 11. If a T2 or T3 work turns up

1. Do not judge it from its abstract. Iteration 13 and D22 both went wrong that way.
2. Get the full text: an open copy, an email to the author, or a PDF you supply.
   *Amendment 2, 11 November 2026 (D35): for A17, full texts are limited to free copies. This was the user's decision of 10 November 2026, because no library access is available (A2) and the schedule allows no waiting for author copies. A candidate whose full text is not free is cited from its abstract, its tier is recorded as unresolved, and it is named in the limitation (§13).*
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

> The literature review is not a systematic review in the PRISMA sense. It combined thirteen rounds of broad, multi-angle web searching ([period]), recorded in a source log but not reproducible query by query, with a structured search fixed in advance and run on [date]: five search strings in two open scholarly indexes, OpenAlex and Semantic Scholar, with a recency check on arXiv[, and in IEEE Xplore's public search interface]; forward-citation searches on eight anchor papers through OpenAlex and Google Scholar; and a patent search in Google Patents. Appendix [X] lists every string exactly as run, with its date and record count. The subscription databases Scopus and Web of Science were not searched, because no institutional access was available. Open indexes lack abstracts for some publishers, so some records could be matched on title alone. Full texts were limited to freely available copies, so [n] candidates that might narrow the claim were judged on their abstracts alone; they are named in the review, with what their abstracts show. One reviewer screened the records, with an AI first pass. Records were screened in English, with four titles in other scripts screened by translation. Patents were screened on their titles by a keyword rule written during the screening, and the pages of 300 of the 1,496 were opened and read through summaries by a language model, Chinese, Korean, Japanese and Taiwanese pages through Google's machine translation; 1,184 were judged on a title alone, so a placement method behind a neutral title could have been missed. The group of operational-technology words in strings S1, S2 and S5 at first had no word for a power network ("power grid", "power system", "electric power"); a supplementary run of those strings and of the patent string with six such words found one more work that narrows the claim, and the patent classification run was not repeated with them. A relevant work indexed only in subscription databases, or described in vocabulary none of the strings anticipated and citing none of the anchor papers, could have been missed. The novelty claim is stated to the best of this search.

*Amendment 2 (D35) changed the limitation above. It replaced "; one reviewer screened the records; and only records with an English title or abstract were screened" with the sentences on free full texts, the AI first pass and translation. For A17's main search, [n] is 8 (`01-search-screening-record.md` §10).*

*Amendments 3–7 (D36) changed the limitation again, as above: "a patent search in Google Patents" (amendment 5: no search was run on the USPTO's Patent Public Search); "four titles in other scripts" for "two" (records 374, 375, 490 and 501); the sentence on patent screening (amendments 4 and 6); and the sentence on the group of operational-technology words (amendment 7). [n] is now 10: the 8 of the main search, and BAG-HRF and Tan et al. (records 419 and 412), whose full texts are not free; the thesis cites them from their abstracts. The two sentences on patent screening and on the operational-technology group are Claude's and the user can strike them with amendments 6 and 7. The user kept both on 16 November 2026 (D37).*

*Amendment 8 (D38) changed the limitation again, as above: "300 of the 1,496" for "262 of the 1,394", "1,184" for "1,128", and the sentence on the group of operational-technology words, which read: "The group of operational-technology words in strings S1, S2 and S5 has no word for a power network ("power grid", "power system", "electric power"), so a work that describes one in those words only was not returned by them." [n] is now 11: the 10 above and Zhan et al. (record 618, `sources.md` #1000), whose full text is not free; the thesis cites it from its abstract.*

**A28's opening clause, once the search and A29's patent sweep have run:** "To the best of a documented search of open scholarly indexes, granted patents and published patent applications, …". *(D37, the user's choice of 16 November 2026; before it: "open scholarly indexes and granted patents".)*

*D36 notes that the patent arm covered published applications as well as grants (the proposed T2, CN 122339846, is both), and proposes "granted patents and published patent applications" for that clause. The wording is the user's (A28); the clause above was unchanged until he decided. D37: he adopted it.*

**Two works not to cite until read in full:** Gusenbauer & Haddaway (#395) and Wohlin (#396).
