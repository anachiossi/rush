/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   count_visible.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: anade-mo <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/22 19:57:19 by anade-mo          #+#    #+#             */
/*   Updated: 2026/03/22 20:03:10 by anade-mo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	count_visible(int sequence[4])
{
	int	max;
	int	i;
	int	visible;

	i = 1;
	max = sequence[0];
	visible = 1;
	while (i < 4)
	{
		if (sequence[i] > max)
		{
			visible++;
			max = sequence[i];
		}
		i++;
	}
	return (visible);
}
/*
int	main(void)
{
	int	sequence[4] = {9, 8, 7, 15}; 
	
	ft_putnbr(count_visible(sequence));
	write(1, "\n", 1);
	return (0);
}*/
