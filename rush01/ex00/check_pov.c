/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   check_pov.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: anade-mo <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/22 17:43:21 by anade-mo          #+#    #+#             */
/*   Updated: 2026/03/22 20:24:51 by anade-mo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	count_visible(int sequence[4]);

int	check_left(int grid[4][4], int clues[16])
{
	int	i;

	i = 0;
	while (i < 4)
	{
		if (count_visible(grid[i]) != clues[8 + i])
			return (0);
		i++;
	}
	return (1);
}

int	check_right(int grid[4][4], int clues[16])
{
	int	i;
	int	j;
	int	sequence[4];

	i = 0;
	while (i < 4)
	{
		j = 0;
		while (j < 4)
		{
			sequence[j] = grid[i][3 - j];
			j++;
		}
		if (count_visible(sequence) != clues[12 + i])
			return (0);
		i++;
	}
	return (1);
}

int	check_top(int grid[4][4], int clues[16])
{
	int	i;
	int	j;
	int	sequence[4];

	i = 0;
	while (i < 4)
	{
		j = 0;
		while (j < 4)
		{
			sequence[j] = grid[j][i];
			j++;
		}
		if (count_visible(sequence) != clues[i])
			return (0);
		i++;
	}
	return (1);
}

int	check_bottom(int grid[4][4], int clues[16])
{
	int	i;
	int	j;
	int	sequence[4];

	i = 0;
	while (i < 4)
	{
		j = 0;
		while (j < 4)
		{
			sequence[j] = grid[3 - j][i];
			j++;
		}
		if (count_visible(sequence) != clues[4 + i])
			return (0);
		i++;
	}
	return (1);
}

int	check_complete(int grid[4][4], int clues[16])
{
	int	top;
	int	bottom;
	int	left;
	int	right;

	top = check_top(grid, clues);
	bottom = check_bottom(grid, clues);
	left = check_left(grid, clues);
	right = check_right(grid, clues);
	if (top && bottom && left && right)
		return (1);
	else
		return (0);
}
