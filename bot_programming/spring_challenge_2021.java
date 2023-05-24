package bot_programming;

import java.util.*;


class Tree {
    int cellIndex;
    int size;
    boolean isMine;
    boolean isDormant;
    public Tree (int cellIndex, int size, boolean isMine, boolean isDormant){
        this.cellIndex = cellIndex;
        this.size = size;
        this.isMine = isMine;
        this.isDormant = isDormant;
    }
}

class Cell {
    int index;
    int richness;
    int neigh0;
    int neigh1;
    int neigh2;
    int neigh3;
    int neigh4;
    int neigh5;
    
    public Cell (int index, int richness, int neigh0, int neigh1, int neigh2, int neigh3, int neigh4, int neigh5){
        this.index = index;
        this.richness = richness;
        this.neigh0 = neigh0;
        this.neigh1 = neigh1;
        this.neigh2 = neigh2;
        this.neigh3 = neigh3;
        this.neigh4 = neigh4;
        this.neigh5 = neigh5;
    }
}

class GameState {
    int day;
    int nutrients;
    int sun;
    int score ;
    int oppSun;
    int oppScore;
    boolean oppIsWaiting;
    public GameState(int day, int nutrients, int sun, int score, int oppSun, int oppScore, boolean oppIsWaiting){
        this.day= day;
        this.nutrients=nutrients; 
        this.sun= sun;
        this.score = score;
        this.oppSun= oppSun;
        this.oppScore= oppScore;
        this.oppIsWaiting= oppIsWaiting;
    }
    public GameState(){}
}

class Player {
    public static void main(String args[]) {
        Scanner in = new Scanner(System.in);
        int numberOfCells = in.nextInt(); // 37
        List<Cell> listOfCells = new ArrayList<Cell>();
        Map<Integer, Tree> mapOfTrees = new HashMap<Integer, Tree>();
        GameState gameState = new GameState();
        for (int i = 0; i < numberOfCells; i++) {
            int index = in.nextInt(); // 0 is the center cell, the next cells spiral outwards
            int richness = in.nextInt(); // 0 if the cell is unusable, 1-3 for usable cells
            int neigh0 = in.nextInt(); // the index of the neighbouring cell for each direction
            int neigh1 = in.nextInt();
            int neigh2 = in.nextInt();
            int neigh3 = in.nextInt();
            int neigh4 = in.nextInt();
            int neigh5 = in.nextInt();
            listOfCells.add(new Cell(index, richness, neigh0, neigh1, neigh2, neigh3, neigh4, neigh5));
        }
        int indexOfTreeFinish = 38;
        int indexOfTreeGrowToThree = 38;
        int indexOfTreeGrowToTwo = 38;
        int indexOfTreeGrowToOne = 38;
        int indexOfTreePlantSeed = 38;
        int countOfTreeFinish = 0;
        // game loop
        while (true) {
            int day = in.nextInt(); // the game lasts 24 days: 0-23
            int nutrients = in.nextInt(); // the base score you gain from the next COMPLETE action
            int sun = in.nextInt(); // your sun points
            int score = in.nextInt(); // your current score
            int oppSun = in.nextInt(); // opponent's sun points
            int oppScore = in.nextInt(); // opponent's score
            boolean oppIsWaiting = in.nextInt() != 0; // whether your opponent is asleep until the next day
            gameState = new GameState(day, nutrients, sun, score, oppSun, oppScore, oppIsWaiting);
            int numberOfTrees = in.nextInt(); // the current amount of trees
            for (int i = 0; i < numberOfTrees; i++) {
                int cellIndex = in.nextInt(); // location of this tree
                int size = in.nextInt(); // size of this tree: 0-3
                boolean isMine = in.nextInt() != 0; // 1 if this is your tree
                boolean isDormant = in.nextInt() != 0; // 1 if this tree is dormant
                mapOfTrees.put(cellIndex, new Tree(cellIndex, size, isMine, isDormant));
                if (isMine){
                    if (size == 3){
                        countOfTreeFinish +=1;
                    }
                    if (size == 3 && cellIndex < indexOfTreeFinish) {
                        indexOfTreeFinish = cellIndex;
                    } else if (size == 2 && cellIndex < indexOfTreeGrowToThree) {
                        indexOfTreeGrowToThree = cellIndex;
                    } else if (size == 1 && cellIndex < indexOfTreeGrowToTwo) {
                        indexOfTreeGrowToTwo = cellIndex;
                    } else if (size == 0 && cellIndex < indexOfTreeGrowToOne) {
                        indexOfTreeGrowToOne = cellIndex;
                    }
                }

            }
            System.err.println(indexOfTreeFinish + " - " +  indexOfTreeGrowToThree + " - " + indexOfTreeGrowToTwo + " - " + indexOfTreeGrowToOne);

            int numberOfPossibleActions = in.nextInt(); // all legal actions
            if (in.hasNextLine()) {
                in.nextLine();
            }
            String possibleAction = "";
            for (int i = 0; i < numberOfPossibleActions; i++) {
                possibleAction = in.nextLine();
                // System.out.println(possibleAction);
            }

            // Write an action using System.out.println()
            // To debug: System.err.println("Debug messages...");
            int remainingRounds = 23 - day;
            System.err.println("r: " + remainingRounds);
            System.err.println("c: " + countOfTreeFinish);
            if (remainingRounds < countOfTreeFinish && indexOfTreeFinish != 38) {
                System.out.println("COMPLETE " + indexOfTreeFinish);
            } else if (indexOfTreeGrowToTwo != 38 && indexOfTreeGrowToOne == 38) {
                List<Integer> neigboursOfTree = new ArrayList<Integer>();
                neigboursOfTree.add(listOfCells.get(indexOfTreeGrowToTwo).neigh0);
                neigboursOfTree.add(listOfCells.get(indexOfTreeGrowToTwo).neigh1);
                neigboursOfTree.add(listOfCells.get(indexOfTreeGrowToTwo).neigh2);
                neigboursOfTree.add(listOfCells.get(indexOfTreeGrowToTwo).neigh3);
                neigboursOfTree.add(listOfCells.get(indexOfTreeGrowToTwo).neigh4);
                neigboursOfTree.add(listOfCells.get(indexOfTreeGrowToTwo).neigh5);
                int currentSmallestIndex  = 38;
                for (int cell_index : neigboursOfTree) {
                    if (cell_index != -1 && listOfCells.get(cell_index).richness !=0 && !mapOfTrees.get(indexOfTreeGrowToTwo).isDormant && !mapOfTrees.containsKey(cell_index)){
                        if (currentSmallestIndex > cell_index) {
                            indexOfTreePlantSeed = cell_index;
                        }
                    }   
                }
                if (indexOfTreePlantSeed != 38)
                {
                     System.out.println("SEED " + indexOfTreeGrowToTwo + " " + indexOfTreePlantSeed);
                } else {
                    System.out.println("GROW " + indexOfTreeGrowToTwo);
                }
            // } else if (indexOfTreeFinish != 38){
            //         System.out.println("COMPLETE " + indexOfTreeFinish);
            } else if (indexOfTreeGrowToThree != 38) {
                System.out.println("GROW " + indexOfTreeGrowToThree);
            } else if (indexOfTreeGrowToTwo != 38) {
                System.out.println("GROW " + indexOfTreeGrowToTwo);
            } else  if (indexOfTreeGrowToOne != 38){
                System.out.println("GROW " + indexOfTreeGrowToOne);
            } else {
                System.out.println("WAIT");
            }
            indexOfTreeFinish = 38;
            indexOfTreeGrowToThree = 38;
            indexOfTreeGrowToTwo = 38;
            indexOfTreeGrowToOne = 38;
            indexOfTreePlantSeed = 38;
            countOfTreeFinish = 0;
        }
    }
}

