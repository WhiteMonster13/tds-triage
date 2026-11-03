# TDS Triage prototype (India, resident payees)

Classifies the *nature of payment* on a vendor invoice (LLM or offline baseline), gates low-confidence/ungrounded answers to a human,
then computes TDS with deterministic code from a versioned rule table. The LLM never produces a rate or an amount.

## Run
    python tds_triage.py --mode baseline                       # offline, no key, no dependencies
    export OPENROUTER_API_KEY=...                              # free-tier key from openrouter.ai
    python tds_triage.py --mode llm --model <a-free-model-id>  # model used: cohere/north-mini-code:free (OpenRouter free tier)

## Files
- rules.json  versioned rule table (ILLUSTRATIVE; marked verify=true where secondary sources disagree on s.393 table item)
- cases.json  14 SYNTHETIC invoices (all made up) with expected category/TDS
- tds_triage.py pipeline: classify -> gate -> calculate

## Results (baseline mode, run offline)
9 correct auto-suggestions, 3 correctly sent to human, 1 needless review, 1 DANGEROUS wrong auto-answer (c10: warehouse space
+ handling services, mixed contract, was labelled rent and showed TDS 0 because it sat under the rent threshold).

## Honest caveats
- The keyword baseline was written by me AFTER seeing the cases, so its score is optimistic. It is a control for the pipeline, not evidence.
- The LLM mode is implemented but NOT yet run by me (no network in my environment). Run it, record the model and results, and
  report where it fails. Do not claim LLM accuracy until you have.
- 14 cases is a smoke test, not a benchmark. Rates/thresholds must be verified by a tax professional.
- Out of scope: non-resident payments (s.393(2)), lower-deduction certificates, s.194Q, TCS, GST.

## LLM results (cohere/north-mini-code:free, temperature 0, single run)
10 correct auto, 3 correct escalations, 0 needless escalations, 1 wrong auto-answer (c04, AMC for ERP software, a grey area the model should have escalated). Full output: results/llm_output.txt
