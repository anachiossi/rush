/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: anade-mo <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 12:12:47 by anade-mo          #+#    #+#             */
/*   Updated: 2026/03/21 13:35:23 by anade-mo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include "rush01.h"

int	main(int argc, char **argv)
{
	int	grid[4][4];
	int	clues[16];
	int	x;
	int	y;

	x = 0;
	if (input_check(argc, argv[1]) == 0)
	{
		write(1, "Error\n", 6);
		return (1);
	}
	input_parse(argv[1], clues);
	while (x < 4)
	{
		y = 0;
		while (y < 4)
		{	grid[y][x] = 0;
			y++;
		}
		x++;
	}
	if (solve(grid, clues, 0) == 0)
	{
		write(1, "Error\n", 6);
		return (1);
	}
	print_grid(grid);
	return (0);
}
