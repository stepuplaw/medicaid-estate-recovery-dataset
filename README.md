# Medicaid Estate Recovery and Home-Transfer Deeds, 50 States and DC (2026)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22922299.svg)](https://doi.org/10.5281/zenodo.22922299)

A state-by-state answer to the question families ask after a parent goes into a nursing home, which is whether the state will take the house after the parent dies. For each of the 50 states and the District of Columbia, the dataset records how far Medicaid estate recovery reaches, and whether recovery can reach a house that passes at death by each of five common methods. The five methods are a traditional life estate, a lady bird deed (an enhanced life estate deed), a transfer on death deed, joint tenancy with right of survivorship, and a revocable living trust.

It also records which states have a transfer on death deed statute, with the effective date, and which states recognize the lady bird deed and on what authority. Every classification cites the statute, regulation, Medicaid manual or State Plan text it rests on, and a saved text copy of that source is in `data/sources/`.

Compiled by [Kevin D. Klagge, Esq.](https://stepuplaw.com/about), a Florida estate planning and elder law attorney (Klagge Law, PLLC). Every row was last verified on September 23, 2026.

- Canonical page with the tables and the citation: <https://stepuplaw.com/data/medicaid-estate-recovery/>
- Source repository: <https://github.com/stepuplaw/medicaid-estate-recovery-dataset>

## What the data shows

Twenty seven jurisdictions limit recovery to the probate estate, 21 states reach property outside probate, and 3 states reach some non-probate property but not all. Probate-only does not mean safe. In 13 probate-only jurisdictions a house in a revocable living trust is still reachable, because the state's trust code makes the trust liable for the settlor's debts when the probate estate is short. In 7 probate-only jurisdictions a transfer on death deed is reachable for the same kind of reason, while a plain life estate is not.

| Method | Reachable | Not reachable | Unclear | Not recognized |
|---|---|---|---|---|
| Traditional life estate | 18 | 32 | 1 | 0 |
| Lady bird deed | 17 | 10 | 24 | 0 |
| Transfer on death deed | 25 | 4 | 6 | 16 |
| Joint tenancy | 22 | 26 | 1 | 2 |
| Revocable trust | 35 | 7 | 9 | 0 |

A house passing by any of the five methods is reachable in 12 states (Kansas, Minnesota, Montana, Nebraska, Nevada, New Hampshire, Ohio, Oregon, Utah, Washington, Wisconsin and Wyoming). In 4 states no method is reachable (Florida, Michigan, Rhode Island and Texas). Florida's answer holds for a homestead, and a non-homestead house held in a revocable trust in Florida is reachable when the probate estate cannot pay the claim.

Thirty four states and the District of Columbia have a transfer on death deed statute. Maryland's takes effect on October 1, 2026, so 33 states and DC have one in force on the verification date. Eight states recognize the lady bird deed on a primary authority, which is a statute in Rhode Island, Vermont and Virginia, case law in Florida, Maryland and Michigan, and a Medicaid agency rule in Texas and North Carolina. West Virginia appears on the popular list of five lady bird states, and no statute, reported case or Medicaid rule recognizing the deed was found there.

`FINDINGS.md` has the full counts, the conflicts with the popular secondary lists, and the ten findings most likely to surprise a reader.

## Files

| Path | Contents |
|---|---|
| `data/states.csv` | One row per jurisdiction (51 rows) |
| `data/states.json` | The same rows as a JSON array |
| `data/schema.json` | Data dictionary as a Frictionless Table Schema, with the allowed values for every coded column |
| `data/datapackage.json` | Frictionless Data Package descriptor for the CSV |
| `data/rows/<CODE>.json` | The per-state files the CSV and JSON are built from |
| `data/sources/<CODE>-<topic>.txt` | Text copies of each statute, rule, manual page or State Plan page relied on. Each file begins with the source URL and the retrieval date. `US-*` files are federal and survey sources, and `US-popular-*` files are the popular secondary lists kept only for comparison. |
| `tools/build.py` | Validates the row files and rebuilds the CSV and JSON |
| `tools/PROTOCOL.md` | The research protocol each state followed |
| `notebooks/estate-recovery-overview.ipynb` | A short notebook that loads the CSV and reproduces the counts above |
| `FINDINGS.md` | Counts, conflicts with popular lists, and key findings |

Rebuild and validate the data with

    python3 tools/build.py          # rebuild states.csv and states.json
    python3 tools/build.py --check  # validate only

## The federal rule behind every row

Federal law, 42 U.S.C. Sec. 1396p(b), requires every state to seek recovery of Medicaid costs from the estates of certain recipients who have died. These are people who were permanently institutionalized, and people who received nursing facility care, home and community based services and related hospital and drug services at age 55 or older.

The floor is the probate estate. Under Sec. 1396p(b)(4)(A), the estate includes at least everything that passes under the state's probate law. A state may go further under Sec. 1396p(b)(4)(B) and reach any property in which the recipient had an interest at death, including property passing by joint tenancy, life estate, living trust or another arrangement. Recovery must wait until a surviving spouse has died, and cannot be made while there is a surviving child under 21 or a blind or disabled child. Every state must also waive recovery for undue hardship.

A state can also place a lien on the home of a permanently institutionalized recipient during life (often called a TEFRA lien), which can reach a house even in a probate-only state. The `recovery_scope_note` column says which states use liens.

## Columns

| Column | Meaning |
|---|---|
| `code`, `name` | Postal code and name |
| `recovery_scope` | `probate_only`, `expanded` (the state adopted the Sec. 1396p(b)(4)(B) option by statute, regulation or controlling case law) or `expanded_partial` (some non-probate assets but not all, explained in the note) |
| `recovery_scope_note` | How the scope was determined, plus liens, recovery from a surviving spouse's estate and service limits |
| `recovery_statute`, `recovery_statute_url` | Governing statute or rule and its official URL |
| `state_plan_4_17_a_url` | Medicaid State Plan Attachment 4.17-A or the agency manual section on estate recovery, where found |
| `life_estate`, `lady_bird_deed`, `tod_deed`, `joint_tenancy`, `revocable_trust` | Whether recovery can reach a house passing this way at the recipient's death, coded `reachable`, `not_reachable`, `unclear` or `n/a` (the method is not recognized in the state) |
| `<method>_note`, `<method>_cite` | A short plain-English reason and the section relied on |
| `tod_deed_recognized`, `tod_deed_statute`, `tod_deed_effective`, `tod_deed_uniform_act` | Whether the state has a transfer on death deed for real property, the statute, the date it took effect, and whether it follows the Uniform Real Property Transfer on Death Act |
| `lady_bird_deed_recognized`, `lady_bird_authority_type`, `lady_bird_authority` | Whether a statute, reported case or state Medicaid rule recognizes a life estate deed with a retained power to sell without the remainder beneficiaries' consent, the kind of authority, and the citation |
| `hardship_waiver_home` | State hardship or deferral rules tied to the home |
| `recovery_exemptions_note` | State protections beyond the federal floor |
| `karp_2005_scope` | How the 2005 AARP survey by Karp, Sabatino and Wood classified the state |
| `last_verified`, `sources`, `confidence`, `flags` | Verification date, the URLs actually read, a confidence grade, and open questions |

The full definitions and allowed values are in `data/schema.json`.

Where lady bird recognition is `unclear`, the `lady_bird_deed` cell says how recovery would treat the deed if a court gave it effect. In an expanded state whose definition covers any life estate or other arrangement, that is usually `reachable`.

## Method

Each jurisdiction was researched from the statute that creates the Medicaid claim and the definition of "estate" in the statute, administrative code, Medicaid manual or State Plan. The scope was then applied to each transfer method, and the state laws that can make a non-probate recipient liable anyway were read too. Those are the creditor section of the transfer on death deed act, the trust code rule on revocable trusts after the settlor's death, and the nonprobate transfer liability statute.

Lady bird recognition requires a primary authority, and practitioner usage alone does not count. Secondary sources such as law firm pages and planning websites were used only to find primary sources, never to fill a cell. Where a legislature's site blocked scripted access, the official page was read through an Internet Archive capture or a Justia, FindLaw or LII copy, and the `flags` column says which. A row graded `high` rests on text read on an official government site, and a row graded `medium` rests on a mirror, an agency manual or a State Plan. No row rests on secondary sources alone.

The Florida row was checked a second time before publication against the Florida statute text and against the published StepUp Law guides on Florida estate recovery and the lady bird deed.

## Not legal advice

This is reference data, not legal advice, and using it creates no attorney-client relationship. Medicaid rules, agency practice and statutes change, and the answer for a particular house depends on facts this table cannot hold, including whether the house is a homestead, who survives the recipient, and whether a lien was recorded during life. Read the cited source before relying on any cell.

## License

The data is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You may use it commercially, modify it and build products on it with credit.

## Citation

Klagge, Kevin D. *Medicaid Estate Recovery and Home-Transfer Deeds, 50 States and DC (2026)*. StepUpLaw, 2026. https://stepuplaw.com/data/medicaid-estate-recovery/

`CITATION.cff` holds the same citation in machine-readable form. Corrections are welcome at office@stepuplaw.com.
