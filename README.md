# Sudoko-Game
Sudoku game featuring AI solving and user input modes, supported by arc consistency and backtracking algorithms for validation and puzzle generation, ensuring an engaging and solvable experience.
### Graphical User Interface (GUI)
The solver boasts a sleek and user-friendly GUI that provides a delightful solving experience. With three distinct modes to choose from, users have the flexibility to engage with the solver in various ways:

1. **Mode 1: Real-Time Solver**
   - Immerse yourself in the solving process as the AI agent dynamically tackles Sudoku puzzles right before your eyes. The visual demonstration offers valuable insights into the strategies employed by the solver.

2. **Mode 2: User Input**
   - Take control of the puzzle-solving journey by inputting your own Sudoku puzzles. Whether you're tackling a handcrafted challenge or working on a puzzle from your favorite magazine, the solver will swiftly provide solutions tailored to your input.

3. **Mode 3 (Bonus): Custom Puzzle Generation**
   - Step into the realm of customization with the bonus mode, which allows you to explore Sudoku puzzles beyond the confines of the traditional 9x9 grid. Experiment with grid sizes ranging from 4x4 to 12x12, unleashing your creativity and problem-solving prowess.

### Algorithmic Approach
Behind the scenes, our solver leverages sophisticated algorithms to efficiently crack Sudoku puzzles:

#### Backtracking
Backtracking serves as the backbone of our solver's functionality, offering essential capabilities for puzzle validation and generation. By employing backtracking, the program ensures the solvability of input puzzles and generates random puzzles with strategically placed initial values, guaranteeing a challenging yet solvable experience.

#### Arc Consistency
At the heart of our solver lies the concept of Arc Consistency, a powerful technique for enforcing puzzle constraints and ensuring solution correctness. Sudoku puzzles are modeled as Constraint Satisfaction Problems (CSPs), where each cell represents a variable with a domain of possible values. Through iterative application of arc consistency, the solver meticulously evaluates and refines the puzzle solution:
- **Representation:** Variables, domains, and constraints form the foundation of the Sudoku CSP, enabling precise representation and analysis of the puzzle.
- **Arc Consistency Enforcement:** By establishing binary constraints between connected variables (cells), the solver systematically evaluates the consistency of each variable's domain, iteratively refining the solution until no further changes can be made.
- **Grid Update:** Following the enforcement of arc consistency, the Sudoku grid undergoes a comprehensive update process, with values assigned to cells based on reduced domain constraints, ultimately leading to the complete solution of the puzzle.

Through the seamless integration of these algorithms, our solver delivers robust and efficient solutions to Sudoku puzzles, offering users a rewarding and intellectually stimulating solving experience.
![Window Screen](https://github.com/Mohamedragih1/Sudoko-AI-Game/assets/93843532/ea022d39-7fe6-452e-b74e-eddfbf5a607b)
![Easy Board](https://github.com/Mohamedragih1/Sudoko-AI-Game/assets/93843532/37072390-9308-444c-b7b1-dd24971caaf1)
![easy board solution](https://github.com/Mohamedragih1/Sudoko-AI-Game/assets/93843532/ed188bee-51fa-4bfe-af7c-58bab0047af5)


