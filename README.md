# CS50 AI Crossword Generator

A Python-based crossword puzzle generator that uses Constraint Satisfaction Problem (CSP) techniques to automatically generate crossword puzzles.

## Project Structure

```
crossword/
├── crossword.py          # Core crossword logic and data structures
├── generate.py           # Main crossword generator with CSP solving
└── data/                 # Puzzle structures and word lists
    ├── structure0.txt    # Small crossword structure
    ├── structure1.txt    # Medium crossword structure  
    ├── structure2.txt    # Large crossword structure
    ├── words0.txt        # Word list for structure0
    ├── words1.txt        # Word list for structure1
    └── words2.txt        # Word list for structure2
```

## Usage

Generate a crossword puzzle:

```bash
python generate.py data/structure0.txt data/words0.txt
```

Save crossword to a text file:

```bash
python generate.py data/structure0.txt data/words0.txt output.txt
```

## Algorithm Implementation

The crossword generator implements a complete CSP solver with:

1. **Node Consistency**: Removes words that don't match variable length constraints
2. **Arc Consistency (AC-3)**: Ensures all binary constraints are satisfied
3. **Backtracking Search**: Uses intelligent variable and value selection heuristics
4. **MRV Heuristic**: Selects variables with minimum remaining values
5. **Degree Heuristic**: Breaks ties by selecting variables with most constraints
6. **Least Constraining Value**: Orders values by how few options they eliminate

## CS50 AI Project

This project is part of the CS50 AI course and demonstrates advanced constraint satisfaction problem solving techniques.
