/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rush01.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: anade-mo <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/03/21 12:58:54 by anade-mo          #+#    #+#             */
/*   Updated: 2026/03/21 14:30:54 by anade-mo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int     input_check(int argc, char *str);
void    input_parse(char *str, int clues[16]);
int     count_visible(int sequence[4]);
int     solve(int grid[4][4], int clues[16], int cell);
void    print_grid(int grid[4][4]);
int     ft_strlen(char *str);
int	ft_putchar(char c);
int	ft_putnbr(int nb);

