/*
 * 
cell: 0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
row:  0  0  0  0  1  1  1  1  2  2  2  2  3  3  3  3
col:  0  1  2  3  0  1  2  3  0  1  2  3  0  1  2  3

0 / 4 = 0
0 % 4 = 0

1 / 4 = 0
1 % 4 = 1

cel = 15
15 / 4 = 3 (row)
15 % 4 = 3 (col)

from main.c cell = 0
*/

int	check_repeat

int	solve(int grid[4][4], int clues[16], int cell)
{
	int	row;
	int	col;
	int	nbr;

	nbr = 1;
	row = cell / 4;
	col = cell % 4;
	if (cell == 16)
		return (1);
	while (nbr <= 4)
	{
		if (nbr != grid[row] && nbr != grid[col])
		{
			grid[row][col] = nbr;
			if (solve(grid, clues, cell + 1) == 1)
				return (1);
		nbr++;
	}
	grid[row][col] = 0;
	return (0);
}

