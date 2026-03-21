/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input_parse.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: anade-mo <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 13:35:53 by anade-mo          #+#    #+#             */
/*   Updated: 2026/03/21 14:33:28 by anade-mo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "rush01.h"
#include <unistd.h>

void	input_parse(char *str, int clues[16])
{
	int	i;
	int	j;

	j = 0;
	i = 0;
	while (str[i])
	{
		if (str[i] != ' ')
		{
			clues[j] = str[i] - '0';
			j++;
		}
		i++;
	}
	return ;
}
/*int	main(void)
{
	int	clues[16];
	int	i;

	i = 0;
	input_parse("4 3 2 1 1 2 2 2 4 3 2 1 1 2 2 2", clues);
	while (i < 16)
	{
		ft_putnbr(clues[i]);
		i++;
	}
	write(1, "\n", 1);
	return (0);
}*/
