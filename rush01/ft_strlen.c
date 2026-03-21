/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlen.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: anade-mo <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/16 13:45:20 by anade-mo          #+#    #+#             */
/*   Updated: 2026/03/16 18:13:21 by anade-mo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
/*ex06
 * Crea una funzione che conta e restituisce
 * il numero di caratteri in una stringa.
 * 	none*/
int	ft_strlen(char *str)
{
	int	i;

	i = 0;
	while (str[i] != '\0')
		i++;
	return (i);
}
