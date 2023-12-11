# importowanie funkcji randint i rand z biblioteki numpy
from numpy.random import randint
from numpy.random import rand

# funkcja celu
def cel(x):
	return x[0]**2.0 + x[1]**2.0

# dekodowanie ciągu bitów na liczby
def rozszyfruj(granice, n_bits, bitstring):
	rozszyfrowane = list()
	najwieksze = 2**n_bits
	for i in range(len(granice)):
		# wyodrębnij podciąg
		poczatek, koniec = i * n_bits, (i * n_bits)+n_bits
		podciag = bitstring[poczatek:koniec]
		# przekształć ciąg bitów na ciąg znaków
		znaki = ''.join([str(s) for s in podciag])
		# przekształć ciąg znaków na liczbę całkowitą
		calkowita = int(znaki, 2)
		# skaluj liczbę całkowitą do pożądanego zakresu
		wartosc = granice[i][0] + (calkowita/najwieksze) * (granice[i][1] - granice[i][0])
		# zapisz
		rozszyfrowane.append(wartosc)
	return rozszyfrowane

# selekcja turniejowa
def selekcja(pop, wyniki, k=3):
	# pierwszy losowy wybór
	selekcja_ix = randint(len(pop))
	for ix in randint(0, len(pop), k-1):
		# sprawdź, czy lepsze
		if wyniki[ix] < wyniki[selekcja_ix]:
			selekcja_ix = ix
	return pop[selekcja_ix]

# krzyżowanie dwóch rodziców w celu wygenerowania dwojga potomków
def krzyzowanie(p1, p2, r_cross):
    # potomkowie domyślnie są kopią rodziców
	c1, c2 = p1.copy(), p2.copy()
	# sprawdzanie w celu rekombinacji
	if rand() < r_cross:
        # wybór punktu krzyżowania, który nie znajduje się na końcu ciągu
		pt = randint(1, len(p1)-2)
		# wykonanie krzyżowania
		c1 = p1[:pt] + p2[pt:]
		c2 = p2[:pt] + p1[pt:]
	return [c1, c2]

# operator mutacji
def mutacja(bitstring, r_mut):
	for i in range(len(bitstring)):
		# sprawdzanie w celu przeprowadzenie mutacji
		if rand() < r_mut:
			# odwrócenie bitu
			bitstring[i] = 1 - bitstring[i]

# algorytm genetyczny
def algorytm_genetyczny(cel, granice, n_bits, n_iter, n_pop, r_cross, r_mut):
	# początkowa populacja losowego ciągu bitowego
	pop = [randint(0, 2, n_bits*len(granice)).tolist() for _ in range(n_pop)]
	# śledzenie najlepszego rozwiązania
	best, best_eval = 0, cel(rozszyfruj(granice, n_bits, pop[0]))
	# wyliczanie pokoleń
	for gen in range(n_iter):
		# rozszyfrowanie populacji
		rozszyfrowane = [rozszyfruj(granice, n_bits, p) for p in pop]
		# ocena wszystkich kandydatów w populacji
		wyniki = [cel(d) for d in rozszyfrowane]
		# sprawdzenie nowych najlepszych rozwiązań
		for i in range(n_pop):
			if wyniki[i] < best_eval:
				best, best_eval = pop[i], wyniki[i]
				print(">%d, nowe najlepsze rozwiązanie f(%s) = %f" % (gen,  rozszyfrowane[i], wyniki[i]))
		# wybór rodziców
		wybrani = [selekcja(pop, wyniki) for _ in range(n_pop)]
		# stworzenie nowej generacji
		dzieci = list()
		for i in range(0, n_pop, 2):
			# połączenie wybranych rodziców w pary
			p1, p2 = wybrani[i], wybrani[i+1]
			# krzyżowanie i mutacja
			for c in krzyzowanie(p1, p2, r_cross):
				# mutacja
				mutacja(c, r_mut)
				# przechowywanie wyników dla następnego pokolenia
				dzieci.append(c)
		# zastąpienie populacji
		pop = dzieci
	return [best, best_eval]

# zakres
granice = [[-5.0, 5.0], [-5.0, 5.0]]
# ilość iteracji
n_iter = 100
# liczba bitów na zmienną
n_bits = 16
# wielkość populacji
n_pop = 100
# współczynnik krzyżowania
r_cross = 0.9
# współczynnik mutacji
r_mut = 1.0 / (float(n_bits) * len(granice))
# przeprowadzenie wyszukiwania algorytmu genetycznego
best, score = algorytm_genetyczny(cel, granice, n_bits, n_iter, n_pop, r_cross, r_mut)
print('Koniec!')
rozszyfrowane = rozszyfruj(granice, n_bits, best)
print('f(%s) = %f' % (rozszyfrowane, score))