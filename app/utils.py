

def disambiguate_referent(referent: str) -> str:
    ref_idx = 1
    ref_split = referent.split("~")
    if len(ref_split) > 1:
        old_idx = int(ref_split[-1])
        ref_idx += old_idx

    return f"{ref_split[0]}~{ref_idx}"