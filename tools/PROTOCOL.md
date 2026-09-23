# Per-state research protocol (for each researcher)

Working folder: `/home/zvi/datasets/estate-recovery-deeds/`. Read `BRIEF.md` first; its Rules are binding. Do not publish, push, email or submit anything. Do not solve CAPTCHAs.

## Output for each state (save after EACH state, before starting the next)
1. `data/rows/<CODE>.json`: one JSON object with exactly the keys in `tools/build.py` COLUMNS (see the Florida row `data/rows/FL.json` as the model once it exists). Leave `karp_2005_scope` as "" (filled centrally).
2. `data/sources/<CODE>-<topic>.txt`: saved text of every statute, regulation, manual or state plan page you relied on. Save with
   `python3 tools/fetch.py <CODE>-<topic> <url> --grep word1 word2` (it strips HTML, reads PDFs, records URL and date, and prints matching lines).
   Topics: `recovery`, `recovery-rule` (admin code), `manual`, `stateplan`, `tod`, `ladybird`, `trust`, `jt`, `hardship`, etc.
   If a site blocks the script (403, CAPTCHA, JS only), try the Justia copy (`law.justia.com/codes/...`) or another official mirror, and mark cells relying on it `medium`. If only WebFetch works, save what WebFetch returned with the Write tool into the same file name and put `Source URL:` / `Retrieved:` / `Note: WebFetch extraction, not verbatim` at the top.
3. Run `python3 tools/build.py --check` and fix any errors for your row.
4. Append one line to `progress.log`:
   `python3 -c "open('progress.log','a').write('<CODE> done confidence=<high|medium|low> <short note>\n')"`

## What to establish per state
- **recovery_scope**: read the state statute (and admin code / manual) that defines "estate" for Medicaid estate recovery.
  - `probate_only`: estate means only assets that pass through the decedent's probate estate (under state probate law).
  - `expanded`: estate includes non-probate assets in which the recipient had legal title or interest at death (the 42 U.S.C. 1396p(b)(4)(B) option: joint tenancy, life estates, living trusts, TOD, etc.).
  - `expanded_partial`: reaches some non-probate assets but not all (e.g., only revocable trusts and joint accounts, or only real property, or expansion enacted but limited). Explain in `recovery_scope_note`.
  - Also note recovery liens under 1396p(a) (TEFRA liens) in the scope note if the state uses them, and whether the state recovers from the surviving spouse's estate.
- **state_plan_4_17_a_url**: search medicaid.gov SPA pages / state Medicaid site for "Attachment 4.17-A" or the Medicaid manual estate recovery section. Blank if not found.
- For each method (life_estate, lady_bird_deed, tod_deed, joint_tenancy, revocable_trust): value `reachable` | `not_reachable` | `unclear` | `n/a`, with `_note` (one or two plain sentences, say WHY, e.g. "Estate limited to probate estate; remainder passes outside probate") and `_cite` (the specific section).
  - Base this on the statutory text. If the statute lists the asset type, cite it. If the state is probate-only, a non-probate transfer is `not_reachable` BUT check for statutes that make that asset liable for the decedent's debts or claims anyway (e.g. revocable trust assets liable for estate claims when the probate estate is insufficient, TOD deed statutes that make the beneficiary liable for claims/statutory allowances, joint account statutes). If such a statute exists and plausibly lets the Medicaid claim reach the asset, use `reachable` or `unclear` and explain.
  - For TOD deed states, READ the TOD deed act's creditor-claim section (URPTODA section 15 equivalent, or the state's own). Many make the beneficiary liable for claims against the transferor's estate to the extent the probate estate is insufficient; some specifically name Medicaid / the state agency. Quote the section number.
  - `n/a` only when the method does not exist in the state (e.g., tod_deed where no TOD deed statute; lady_bird_deed where the state clearly does not recognize it).
  - A home-specific rule (e.g. recovery limited to the home, or the home excluded) matters; note it.
- **tod_deed_recognized / tod_deed_statute / tod_deed_effective / tod_deed_uniform_act**: from the statute itself (effective date from session law / history note). `tod_deed_uniform_act` = yes if the state enacted the Uniform Real Property Transfer on Death Act (check the statute's short title or history; the ULC enactment list at uniformlaws.org may point you there). Record act or chapter number in the note/flags for anything effective 2024 to 2026.
- **lady_bird_deed_recognized / lady_bird_authority_type / lady_bird_authority**: `yes` only if a statute, reported case, state title standard or state Medicaid rule recognizes a life estate deed with a retained power to sell/convey without the remainder's consent. `lady_bird_authority_type`: `statute`, `case_law`, `agency_rule` (Medicaid manual treats it), `practice` (only practitioner usage, no primary authority found), `none`, `unclear`. Give the citation. If you found no primary authority, say `unclear` and what you searched.
- **hardship_waiver_home**: state-specific hardship or deferral rules tied to the home (modest-value homestead, caregiver child, sibling, income-producing property, family farm). Cite.
- **recovery_exemptions_note**: only state additions beyond the federal floor (e.g., recovery deferred until death of surviving spouse is federal; note state extras such as recovery only for 55+ nursing care, exemptions for small estates, American Indian property, etc.).
- **sources**: semicolon list of URLs you actually read. **last_verified**: 2026-09-23 (today). **confidence**: `high` only if the operative statute text (recovery definition) was read on an official site; `medium` if from Justia/Casetext or agency manual/state plan only; `low` if secondary only. **flags**: anything uncertain, recent amendments (2024 to 2026, with act/chapter number and effective date), conflicts between statute and manual.

## Rules
- Never write statute text or a classification from memory. Everything must be traced to a page you read in this session. Secondary sources (law firm blogs, medicaidlongtermcare.org, medicaidplanningassistance.org, nolo) may only point you to primary sources.
- US style, plain English, short notes. NO em dashes or en dashes anywhere (use commas, colons, or "to"). Use "Sec." or the section sign as you like, but be consistent: prefer "Sec." e.g. "Ohio Rev. Code Sec. 5162.21(F)".
- Check for 2024 to 2026 amendments (search "<state> estate recovery 2025 bill", "<state> transfer on death deed 2026"). Maryland TOD deeds effective Oct 1, 2026; Georgia and New York enacted TOD deeds in 2024: verify exact dates and act numbers from the session law.
- Keep web usage reasonable: about 10 to 25 fetches per state.
- Final message back to the coordinator: for each state, one line: code, scope, the five method values, TOD yes/no + date, lady bird value + type, confidence, and any major surprise or conflict with popular lists.
