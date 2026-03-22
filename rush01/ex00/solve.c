/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   solve.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: anade-mo <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/22 20:03:52 by anade-mo          #+#    #+#             */
/*   Updated: 2026/03/22 20:26:37 by anade-mo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	check_complete(int grid[4][4], int clues[16]);

int	check_repeat(int grid[4][4], int col, int row, int nbr)
{
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

int	solve(int grid[4][4], int clues[16], int cell)
{
	int	row;
	int	col;
	int	nbr;

	nbr = 1;
	row = cell / 4;
	col = cell % 4;
	if (cell == 16 && check_complete(grid, clues))
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
