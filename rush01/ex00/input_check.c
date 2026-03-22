/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   input_check.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: anade-mo <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 08:42:04 by anade-mo          #+#    #+#             */
/*   Updated: 2026/03/22 19:49:22 by rferraro         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <unistd.h>

int	ft_strlen(char *str);

int	input_check(int argc, char *str)
{
	int	i;
	int	expected;

	i = 0;
	expected = 1;
	if (argc != 2)
		return (0);
	if (ft_strlen(str) != 31)
		return (0);
	while (str[i])
	{
		if (!((expected && (str[i] >= '1' && str[i] <= '4'))
				|| (!expected && str[i] == ' ')))
			return (0);
		if ((str[i] < '1' || str[i] > '4') && (str[i] != ' '))
			return (0);
		expected = !expected;
		i++;
	}
	return (1);
}
/*
int	main(int argc, char **argv)
{
	if (input_check(argc, argv[1]) == 0)
		write(1, "ERROR\n", 6);
	return (0);
}*/
