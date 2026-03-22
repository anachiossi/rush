/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: anade-mo <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 12:12:47 by anade-mo          #+#    #+#             */
/*   Updated: 2026/03/22 20:32:24 by anade-mo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

int		input_check(int argc, char *str);
void	input_parse(char *str, int clues[16]);
int		solve(int grid[4][4], int clues[16], int cell);
void	print_grid(int grid[4][4]);

int	init(int argc, char **argv)
{
	if (input_check(argc, argv[1]) == 0)
	{
		write(1, "Error\n", 6);
		return (1);
	}
	return (0);
}

int	last_check(int grid[4][4], int clues[16], int cell)
{
	if (solve(grid, clues, cell) == 0)
	{
		write(1, "Error\n", 6);
		return (1);
	}
	return (0);
}

int	main(int argc, char **argv)
{
	int	grid[4][4];
	int	clues[16];
	int	x;
	int	y;

	x = 0;
	if (init(argc, argv) == 1)
		return (1);
	input_parse(argv[1], clues);
	while (x < 4)
	{
		y = 0;
		while (y < 4)
		{
			grid[y][x] = 0;
			y++;
		}
		x++;
	}
	if (last_check(grid, clues, 0) == 1)
		return (1);
	print_grid(grid);
	return (0);
}
