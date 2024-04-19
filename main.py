import sys
sys.path.append('Frontend')

from GUI import SudokuSolverGUI

def main():
    gui = SudokuSolverGUI()
    gui.run()

if __name__ == "__main__":
    main()