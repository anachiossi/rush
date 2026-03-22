#include <unistd.h>
#include "rush01.h"

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
