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

int	check_repeat(int grid[4][4], int col, int row, int nbr)
{
}
	int	i;
	
	i = 0;
	while (i < 4)
	{
		if (grid[row][i] == nbr)
			return (1);
		i++;
	}
	i = 0;
	while (i < 4)
	{
		if (grid[i][col] == nbr)
			return (1);
		i++;
	}
	return (0);
}

int	check_rows(int grid[4][4], int clues[16])
{
	int	i++;
	int	j++;
	int	sequence[4];

	i = 0;
	while (i < 4) //row 00, 01, 02, 03, left 8a11] //
	{
		if (count_visible(grid[i]) != clues[8 + i])
			return (0);
		i++;
	}
	i = 0;
	while (i < 4) //row 03, 02, 01, 00. right 12a15 //
	{
		j = 0;
		while (j < 4)
		{
			sequence[j] = grid[i][3 - j]
			j++;
		}
		if (count_visible(sequence) != clues[12 + i])
			return (0);
		i++;
	}
	return (1);
}
//stoped here, realized check grid was too long so i split in chec rows, check cols
		
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
		if (check_repeat(grid, col, row, nbr) == 0)
		{
			grid[row][col] = nbr;
			if (solve(grid, clues, cell + 1) == 1)
			return (1);
		}
		nbr++;
	}
	grid[row][col] = 0;
	return (0);
}

