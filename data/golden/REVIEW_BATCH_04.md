**Status: FROZEN (v1 golden set)**

# Review Batch 04 — Candidates for human review

**Status:** Candidates only (post 4-query revision). Not frozen. Not in seed/corpus.

## Methodology (frozen — same as Batch 01–03)
- Full judgment body text
- Gold = judgment_id + char_start/char_end
- Light cleaning only
- Scoring: overlap ≥100 chars OR ≥30% of span

## Counts: **14 queries**, **14 spans**, **7 judgments**
## Difficulty: {'easy': 4, 'medium': 6, 'hard': 4}

## Judgments

- `2023_11_76_85` — M/s Isnar Aqua Farms v. United India Insurance Co. Ltd. — *insurance / marine risk*
- `2023_1_433_442` — Gas Point Petroleum India Ltd. v. Rajendra Marothi — *CPC Order XXI / execution*
- `2023_2_6_11` — Vikas Rathi v. State of U.P. — *CrPC / quashing*
- `2023_4_51_62` — Registrar General, High Court of Karnataka v. M. Narasimha Prasad — *service law / judicial officers*
- `2023_6_831_850` — K. Chinnammal v. L. R. Eknath — *tenancy / cultivating tenants*
- `2023_2_875_880` — Pawan Kumar Chourasia v. State of Bihar — *criminal evidence / extra-judicial confession*
- `2023_1_231_240` — Basavaraj v. Padmavathi — *specific performance*

## Per-query spans

### q_ins4_01 [easy/civil]
Q: What rate of interest did the Supreme Court hold to be just and equitable on the insurance claim amount awarded by the NCDRC?
- `2023_11_76_85` [16636:17113] That being so, the interest rate fi xed by the NCDRC, viz, 10% is held to be just and equitable. 16. The sum of ` 45,18,263.20 shall be remitted by th...

### q_ins4_02 [medium/civil]
Q: What directions were issued regarding remittance of the insurance claim amount with interest?
- `2023_11_76_85` [16737:17177] The sum of ` 45,18,263.20 shall be remitted by the respondent insurance company to the appellant, with simple interest thereon @ 10% from the date of ...

### q_cpc_01 [medium/civil]
Q: When an auction purchaser fails to deposit 25% of the sale amount immediately, what is the legal consequence for the court auction sale?
- `2023_1_433_442` [16947:17468] We hold, therefore, that in the circumstances of the present case there was no sale and the purchasers acquired no rights at all.” 8.3 Applying the la...

### q_cpc_02 [hard/civil]
Q: Can objections by an auction purchaser be sustained when the mandatory deposit requirement under the execution sale process was not complied with?
- `2023_1_433_442` [19352:19904] consequently the order passed by the Executing Court overruling t he objections raised by the appellant also deserves to be quash ed and set aside and...

### q_crpc4_01 [medium/criminal]
Q: What is the standard for summoning an additional accused under Section 319 CrPC based on evidence recorded during trial?
- `2023_2_6_11` [5463:6041] and not in a casual and cavalier manner. 106. Thus we hold that though only a prima facie case is to be established from the evidence laid before the ...

### q_crpc4_02 [hard/criminal]
Q: If a trial court order under Section 319 CrPC is imperfectly worded, should the High Court quash it entirely or correct the error in revision?
- `2023_2_6_11` [9568:10025] High Court, but that error could have been corrected in exercise of revisional power. 16. For the reasons mentioned above, the present appeal is allow...

### q_svc4_01 [hard/service]
Q: When a Division Bench sets aside dismissal of a judicial officer, what standard of review applies to the Full Court's disciplinary decision?
- `2023_4_51_62` [6512:7464] 17. While considering a challenge to an order of penalty imposed upon a judicial officer pursuant to the disciplinary proceedings followed by a resolu...

### q_svc4_02 [medium/service]
Q: Can disciplinary proceedings against a judicial officer be shut down on the ground that no further inquiry can be held after certain procedural stages?
- `2023_4_51_62` [10741:11939] We have not come across a case where the High Court, while setting aside an order of penalty has held that there sh all not be any further inquiry aga...

### q_ten_01 [hard/civil]
Q: What are the limits on the High Court’s supervisory jurisdiction under Article 227 when reviewing orders in cultivating tenants matters?
- `2023_6_831_850` [34357:34891] contrary to law and cannot be sustained for several reasons, but primarily for deviation from the limited jurisd iction exercised by the High Court un...

### q_ten_02 [easy/civil]
Q: Did the Supreme Court find any infirmity in the Impugned Judgment and the Revenue Court orders regarding the cultivating tenants dispute?
- `2023_6_831_850` [35979:36400] On an overall circumspection of the facts and circumstances, this Court does not find any infirmity in Impugned Judgment, and the Orders dated 04.02.2...

### q_evi_01 [easy/criminal]
Q: Can a conviction rest solely on an extra-judicial confession that the appellate court finds deserves to be discarded, with no other evidence?
- `2023_2_875_880` [8582:9073] form of the extra-judicial confession of the appellant deserv es to be discarded. Admittedly, there is no other evidence against the appellant. Theref...

### q_evi_02 [medium/criminal]
Q: Is corroboration of an extra-judicial confession required as a matter of rule under Indian evidence law?
- `2023_2_875_880` [3741:4312] confession keeping in view the circumstances in which it is made. As a matter of rule, corroboration is not required. However, if an extra-judicial co...

### q_sp_01 [medium/civil]
Q: What must a plaintiff prove regarding readiness and willingness in a suit for specific performance of a contract for sale of land?
- `2023_1_231_240` [12296:16235] High Court has materially erred in reversing the decree by reversing the findings of the Trial Court on readiness and willingness of the appellant. 6....

### q_sp_02 [easy/civil]
Q: When specific performance is decreed, what directions may the Supreme Court give regarding deposit and withdrawal of the balance sale consideration?
- `2023_1_231_240` [17118:17554] Defendant No. 1 shall also be permitted to withdraw the amount i.e., Rs. 9,74,000/- deposited by the plaintiff on 31.10.2011, pursuant to the judgment...

## Files
- review_batch_04_queries.jsonl
- review_batch_04_judgments.jsonl
- seed/corpus: **untouched**

---
**v1 FROZEN GOLDEN SET** — promoted 2026-10-05. Do not edit labels.
