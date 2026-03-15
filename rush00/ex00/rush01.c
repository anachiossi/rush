/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rush01.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: anade-mo <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/15 17:03:57 by anade-mo          #+#    #+#             */
/*   Updated: 2026/03/15 17:11:40 by anade-mo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putchar(char c);

void	print_line(int columns, char start, char mid, char end)
{
	if (columns < 1)
	{
		return ;
	}
	ft_putchar(start);
	columns--;
	while (columns > 1)
	{
		ft_putchar(mid);
		columns--;
	}
	if (columns > 0)
	{
		ft_putchar(end);
	}
	ft_putchar('\n');
}

void	rush(int x, int y)
{
	int	row;

	row = 1;
	while (row <= y)
	{
		if (row == 1)
		{
			print_line(x, '/', '*', '\\');
		}
		else if (row == y)
		{
			print_line(x, '\\', '*', '/');
		}
		else
		{
			print_line(x, '*', ' ', '*');
		}
		row++;
	}
}
