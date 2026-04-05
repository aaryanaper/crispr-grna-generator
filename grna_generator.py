def find_grnas(sequence, mutation_pos, mutant_nt, window=40):
    sequence = sequence.upper().strip()
    mutant_nt = mutant_nt.upper().strip()

    if not (100 <= len(sequence) <= 120):
        raise ValueError(f"Sequence length must be between 100 and 120. Got {len(sequence)}")

    if any(ch not in "ATCG" for ch in sequence):
        raise ValueError("Sequence must contain only A, T, C, and G")

    if mutant_nt not in {"A", "T", "C", "G"}:
        raise ValueError("Mutant nucleotide must be one of A, T, C, or G")

    if not (1 <= mutation_pos <= len(sequence)):
        raise ValueError("Mutation position is out of range")

    mutation_idx = mutation_pos - 1
    wildtype_base = sequence[mutation_idx]

    if wildtype_base == mutant_nt:
        raise ValueError("Mutant nucleotide must be different from the wild-type base")

    # Build mutant string by replacing the base at the mutation position
    mutant_sequence = sequence[:mutation_idx] + mutant_nt + sequence[mutation_idx + 1:]

    # Search for PAMs near the mutation
    start = max(0, mutation_idx - window)
    end = min(len(mutant_sequence) - 2, mutation_idx + window + 1)

    candidates = []

    for i in range(start, end):
        pam = mutant_sequence[i:i+3]

        # Find NGG PAMs only in the given string
        if len(pam) == 3 and pam[1:] == "GG":
            guide_start = i - 20
            guide_end = i

            # Need a full 20-character guide to the left of the PAM
            if guide_start < 0:
                continue

            # Keep only if the mutation lies inside the guide
            if not (guide_start <= mutation_idx < guide_end):
                continue

            guide = mutant_sequence[guide_start:guide_end]
            full_target = guide + pam
            mutation_pos_in_guide = (mutation_idx - guide_start) + 1  # 1-based

            if mutation_pos_in_guide >= 11:
                classification = "high-stringency (PAM-proximal)"
            else:
                classification = "moderate-stringency (PAM-distal)"

            candidates.append({
                "guide": guide,
                "pam": pam,
                "full_target": full_target,
                "mutation_pos_in_guide": mutation_pos_in_guide,
                "classification": classification,
                "pam_location": f"{i+1}-{i+3}"
            })

    # Sort so guides with mutation closer to PAM come first
    candidates.sort(key=lambda x: -x["mutation_pos_in_guide"])

    return {
        "sequence_length": len(sequence),
        "wildtype_base": wildtype_base,
        "mutant_sequence": mutant_sequence,
        "candidates": candidates
    }