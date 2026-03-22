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

int		input_check(int argc, char *str); //checks in input is preciselly ok
void	input_parse(char *str, int clues[16]); //transforms string into int array 16 = clues[16]
int		solve(int grid[4][4], int clues[16], int cell); //backtracking logic to fill and test 
void	print_grid(int grid[4][4]); //prints the grid line by line

int	init(int argc, char **argv) //runs the program and takes the string from terminal
{
	if (input_check(argc, argv[1]) == 0) //if input check find errors 
	{
		write(1, "Error\n", 6); 
		return (1);
	}
	return (0); 
}

int	last_check(int grid[4][4], int clues[16], int cell) //sends all info to be solved from cell 0, if it has no solution prints error 
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
	if (init(argc, argv) == 1) //if input is not ok, closes.
		return (1);
	input_parse(argv[1], clues); //if input is ok sends it to be transformed and organized
	while (x < 4) // creates a grid[4][4] and populate it with zero, so is not random.
	{
		y = 0;
		while (y < 4)
		{
			grid[y][x] = 0;
			y++;
		}
		x++;
	}
	if (last_check(grid, clues, 0) == 1) //inicializate solution mechanism and if fails, closes.
		return (1);
	print_grid(grid); //if solved worked, print the solution
	return (0); //successfull closure :)
}
