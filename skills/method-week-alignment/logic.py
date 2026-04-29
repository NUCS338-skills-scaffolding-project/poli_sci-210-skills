# logic.py — method-week-alignment
# Granular skill in Phase 2 (extract-research-design). Tracks whether the
# student has logged at least 2 method-specific concerns from the appropriate
# checklist, each tied to a specific paper element with an alignment label,
# and that the concerns span more than one sub-family. Pure function; no side
# effects.

VALID_METHODS = (
  "theory-data",
  "inference",
  "surveys",
  "experiments",
  "large-n",
  "small-n",
  "machine-learning",
)

VALID_ALIGNMENT = ("addressed", "partially addressed", "unaddressed")
MIN_CONCERNS = 2
TARGET_CONCERNS = 4
MIN_ELEMENT_WORDS = 4
MIN_NOTE_WORDS = 4

# Sub-family keyword tags per method. Heuristic only: a concern's text is
# tagged with whichever family's keyword appears first. If two concerns share
# the same family, that's clustering.
FAMILY_KEYWORDS = {
  "theory-data": {
    "falsifiability": ("falsifia", "refut", "test logic"),
    "operationalization": ("operationaliz", "measure", "concept"),
    "scope": ("scope", "boundary", "domain"),
    "data-quality": ("data sourc", "data quality", "transparency", "provenance"),
    "alternative-theory": ("alternative theor", "rival explanation"),
  },
  "inference": {
    "identification": ("identification", "did", "iv", "rdd", "matching", "selection-on-observables"),
    "counterfactual": ("counterfactual", "comparison group", "control"),
    "threats": ("confound", "selection bias", "reverse causation", "measurement error"),
    "scope": ("scope", "external validity", "generaliz"),
    "robustness": ("robust", "alternative specification"),
    "heterogeneity": ("heterogen", "subgroup"),
  },
  "surveys": {
    "sampling": ("sampling frame", "sample selection", "representative"),
    "response-rate": ("response rate", "non-response", "nonresponse"),
    "wording": ("question wording", "framing", "item wording"),
    "scale": ("response scale", "scale point", "likert"),
    "mode": ("mode effect", "phone", "online", "in-person"),
    "weighting": ("weight", "poststratif"),
    "pre-registration": ("pre-regist", "preregist", "robustness across"),
  },
  "experiments": {
    "randomization": ("randomiz", "balance check", "assignment"),
    "compliance": ("compliance", "uptake", "treatment delivery"),
    "attrition": ("attrition", "dropout"),
    "sutva": ("sutva", "spillover", "interference"),
    "external-validity": ("external validity", "generaliz", "setting", "duration", "dose"),
    "outcome-measurement": ("outcome measure", "measurement timing", "instrument"),
    "pre-registration": ("pre-regist", "preregist"),
  },
  "large-n": {
    "sample-period": ("sample period", "time window", "panel"),
    "case-selection": ("case selection", "country selection", "universe"),
    "specification": ("specification", "fixed effects", "controls", "interaction"),
    "standard-errors": ("standard error", "clustering", "robust", "bootstrap"),
    "robustness": ("robustness", "alternative specification"),
    "generalization": ("generaliz", "external validity"),
    "outliers": ("outlier", "influential observation"),
  },
  "small-n": {
    "case-selection": ("case selection", "typical", "deviant", "most-likely", "least-likely"),
    "process-tracing": ("process tracing", "within-case", "causal-process observation"),
    "comparative-logic": ("comparative", "across cases", "single case rationale"),
    "alternatives": ("alternative explanation", "rival"),
    "generalization": ("generaliz", "scope"),
    "sources": ("source", "triangulation", "bias"),
  },
  "machine-learning": {
    "training-data": ("training data", "label provenance", "leakage"),
    "metric": ("evaluation metric", "metric"),
    "split": ("train/test split", "temporal split", "blocked split", "clustered split"),
    "baseline": ("baseline", "simpler model", "human comparison"),
    "interpretation": ("interpretation", "substantive question"),
    "generalization": ("out-of-sample", "out of sample", "generaliz"),
    "fairness": ("fairness", "disparate", "subgroup"),
  },
}


def _entry_complete(entry):
  if not isinstance(entry, dict):
    return False
  concern = (entry.get("concern") or "").strip()
  paper_element = (entry.get("paper_element") or "").strip()
  alignment = (entry.get("alignment") or "").strip().lower()
  note = (entry.get("note") or "").strip()
  if not concern:
    return False
  if len(paper_element.split()) < MIN_ELEMENT_WORDS:
    return False
  if alignment not in VALID_ALIGNMENT:
    return False
  if len(note.split()) < MIN_NOTE_WORDS:
    return False
  return True


def _family_for(concern_text, method):
  blob = concern_text.lower()
  families = FAMILY_KEYWORDS.get(method, {})
  for family, kws in families.items():
    if any(kw in blob for kw in kws):
      return family
  return None


def run(input):
  """
  :param input: {
    "week": int,
    "method": str,
    "article_path": str,
    "prior_session_logs": list[str] | None,
    "prior_in_phase_scratchpads": dict[str, str] | None,
    "concerns": list[{
      "concern": str,
      "paper_element": str,
      "alignment": str,                # "addressed" | "partially addressed" | "unaddressed"
      "note": str,
    }] | None,
  }
  :return: {
    "complete_count": int,
    "incomplete_count": int,
    "families_represented": list[str | None],
    "all_one_family": bool,
    "next_prompt": str,
    "done": bool,
    "done_reasons": list[str],
    "observations": list[str],
  }
  """
  if not isinstance(input, dict):
    raise ValueError("input must be a dict")

  method = input.get("method")
  if method not in VALID_METHODS:
    raise ValueError(f"method={method!r} must be one of {VALID_METHODS}")

  concerns = input.get("concerns") or []
  if not isinstance(concerns, list):
    raise ValueError("concerns must be a list")

  complete = [c for c in concerns if _entry_complete(c)]
  incomplete = [c for c in concerns if not _entry_complete(c)]
  families = [_family_for(c.get("concern", ""), method) for c in complete]

  unique_families = {f for f in families if f is not None}
  all_one_family = (
    len(complete) >= 2
    and len(unique_families) == 1
  )

  if len(complete) == 0 and len(incomplete) == 0:
    next_prompt = "show_checklist_and_ask_first"
  elif len(incomplete) > 0:
    last = incomplete[-1]
    if not (last.get("concern") or "").strip():
      next_prompt = "ask_concern"
    elif len((last.get("paper_element") or "").split()) < MIN_ELEMENT_WORDS:
      next_prompt = "ask_paper_element"
    elif (last.get("alignment") or "").strip().lower() not in VALID_ALIGNMENT:
      next_prompt = "ask_alignment"
    elif len((last.get("note") or "").split()) < MIN_NOTE_WORDS:
      next_prompt = "ask_note"
    else:
      next_prompt = "ask_next_concern"
  elif len(complete) < MIN_CONCERNS:
    next_prompt = "ask_next_concern"
  elif all_one_family:
    next_prompt = "push_different_family"
  elif len(complete) < TARGET_CONCERNS:
    next_prompt = "offer_more_concerns"
  else:
    next_prompt = "reconcile_and_exit"

  done = (
    len(complete) >= MIN_CONCERNS
    and not all_one_family
  )

  done_reasons = []
  if len(complete) >= MIN_CONCERNS:
    done_reasons.append(f"{len(complete)} substantive concern(s) logged with paper-specific elements")
  if not all_one_family:
    done_reasons.append("concerns span more than one sub-family (or families could not be tagged)")

  observations = [
    f"Method: {method}.",
    f"Complete entries: {len(complete)} (need {MIN_CONCERNS}, target {TARGET_CONCERNS}).",
    f"Incomplete entries: {len(incomplete)}.",
    f"Families represented: {sorted({f for f in families if f is not None}) or 'none-tagged'}.",
  ]
  if all_one_family:
    observations.append(
      f"All concerns in family '{list(unique_families)[0]}' — push the student to a different family."
    )
  observations.append(f"Next tutor move: {next_prompt}.")

  # LLM stub: a semantic check would do the family-tagging more robustly than
  # keyword matching, would catch concerns that don't actually come from this
  # week's checklist, and would flag alignment labels that disagree with the
  # paper's actual handling of the concern.
  return {
    "complete_count": len(complete),
    "incomplete_count": len(incomplete),
    "families_represented": families,
    "all_one_family": all_one_family,
    "next_prompt": next_prompt,
    "done": done,
    "done_reasons": done_reasons,
    "observations": observations,
  }
