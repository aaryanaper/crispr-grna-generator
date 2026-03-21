def find_grnas(sequence, mutation_pos, window=20):
    """
    sequence: DNA string (A, T, C, G)
    mutation_pos: index of mutation (0-based)
    window: how far around mutation to search
    """
    sequence = sequence.upper()
    grnas = []

    start = max(0, mutation_pos - window)
    end = min(len(sequence), mutation_pos + window)

    for i in range(start, end - 2):
        pam = sequence[i:i+3]

        # Check for NGG PAM
        if pam[1:] == "GG":
            guide_start = i - 20
            guide_end = i

            if guide_start >= 0:
                guide = sequence[guide_start:guide_end]

                grnas.append({
                    "guide": guide,
                    "pam": pam,
                    "position": i
                })

    return grnas


# Example usage
if __name__ == "__main__":
    dna = input("Enter DNA sequence (120 nt): ")
    mutation = int(input("Enter mutation position (0-based index): "))

    results = find_grnas(dna, mutation)

    print("\nPossible gRNAs:")
    for r in results:
        print(f"Guide: {r['guide']} | PAM: {r['pam']} | Position: {r['position']}")