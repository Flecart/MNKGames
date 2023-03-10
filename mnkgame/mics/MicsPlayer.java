package mnkgame.mics;

import java.util.ArrayList;
import java.util.Collections;

import mnkgame.MNKCell;
import mnkgame.MNKCellState;
import mnkgame.MNKGameState;

public class MicsPlayer implements mnkgame.MNKPlayer {
    private Board B;
    private MNKGameState myWin;
    private MNKCellState myState;
    private MNKCellState yourState;
    private MNKGameState yourWin;
    private ArrayList<CellPair> moves;

    public MicsPlayer() {}

    public void initPlayer(int M, int N, int K, boolean first, int timeout_in_secs) {
        myState = first ? MNKCellState.P1 : MNKCellState.P2;
        yourState = first ? MNKCellState.P2 : MNKCellState.P1;
        B = new Board(M, N, K, myState);
        myWin = first ? MNKGameState.WINP1 : MNKGameState.WINP2;
        yourWin = first ? MNKGameState.WINP2 : MNKGameState.WINP1;

        moves = new ArrayList<CellPair>();
    }

    // time should never run out right? it's the first step!
    // @returns a winning cell if there is one
    private MNKCell findWinCell(MNKCell[] freeCells) {
        for (MNKCell d : freeCells) {
            if (B.markCell(d.i, d.j) == myWin) {
                return d;
            } else {
                B.unmarkCell();
            }
        }
        return null;
    }

    private MNKCell findPreventWinCell(MNKCell[] freeCells) {
        for (MNKCell d : freeCells) {
            if (B.markCell(d.i, d.j) == yourWin) {
                B.unmarkCell();
                
                // vado a marcare io la cella con cui vincerebbe l'avversario
                B.setPlayer(myState);;
                B.markCell(d.i, d.j);
                return d;
            }
            B.unmarkCell();
        }
        return null;
    }

    private int getWholeHeuristics(MNKCell freeCell) {
        return B.getHeuristic(freeCell.i, freeCell.j) + B.getSwappedHeuristics(freeCell.i, freeCell.j);
    }

    public MNKCell selectCell(MNKCell[] freeCells, MNKCell[] movedCells) {
        B.setPlayer(yourState);
        if (movedCells.length > 0) {
            MNKCell c = movedCells[movedCells.length - 1]; // Recover the last move from MC
            B.markCell(c.i, c.j); // Save the last move in the local MNKBoard
        }

        B.setPlayer(myState);
        MNKCell winCell = findWinCell(freeCells);
        if (winCell != null) return winCell;

        B.setPlayer(yourState);
        MNKCell preventWinCell = findPreventWinCell(freeCells);
        if (preventWinCell != null) return preventWinCell;

        for (int i = 0; i < freeCells.length; i++)
            moves.add(new CellPair(getWholeHeuristics(freeCells[i]), freeCells[i]));

        Collections.sort(moves);
        MNKCell bestCell = moves.get(0).cell;
        B.setPlayer(myState);
        B.markCell(bestCell.i, bestCell.j);
        moves.clear();
        return bestCell;
    }

    public String playerName() {
        return "Mics Player";
    }
}
