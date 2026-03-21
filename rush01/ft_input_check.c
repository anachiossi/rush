/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_input_check.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: anade-mo <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 08:42:04 by anade-mo          #+#    #+#             */
/*   Updated: 2026/03/21 09:10:25 by anade-mo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include <unistd.h>

int	ft_strlen(char *str);

int	ft_input_check(int argc, char *str)
{
	int	i;

	i = 0;
	if (argc != 2)
		return (0);
	if (ft_strlen(str) != 31)
		return (0);
	while (str[i])
	{
		if ((str[i] < '1' || str[i] > '4') 
				&& (str[i] != ' '))
			return (0);
		i++;
	}
	return (1);
}

int	main(int argc, char **argv)
{
	ft_input_check(argc, argv[1]);
}
