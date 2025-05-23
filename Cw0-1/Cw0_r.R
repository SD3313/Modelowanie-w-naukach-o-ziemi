# Instalujemy wymagane biblioteki
if(!require(animation)) install.packages("animation")
if(!require(fields)) install.packages("fields")

library(animation)
library(fields)

# Tworzymy dwie macierze zerowe 10x10
L <- matrix(0, nrow = 10, ncol = 10)
Lnew <- matrix(0, nrow = 10, ncol = 10)

# Ustalamy warunek początkowy - rozgrzana dolna powierzchnia
L[10, ] <- 1
Lnew[10, ] <- 1

# Funkcja do sprawdzania warunku zatrzymania
stop_condition <- function(L, Lnew) {
  return(abs(sum(Lnew) - sum(L)))
}

# Lista na przechowywanie kolejnych iteracji
data_frames <- list()

# Główna funkcja obliczająca równanie Laplace'a
laplace <- function(L, Lnew) {
  e <- 1
  while (e > 0.01) {
    for (i in 2:9) {
      for (j in 2:9) {
        Lnew[i, j] <- 0.25 * (L[i-1, j] + L[i+1, j] + L[i, j-1] + L[i, j+1])
      }
    }

    e <- stop_condition(L, Lnew)

    data_frames[[length(data_frames) + 1]] <- Lnew
    L[] <- Lnew
  }

  return(data_frames)
}

# Wywołujemy funkcję laplace
data_frames <- laplace(L, Lnew)

# Funkcja do wyświetlania animacji
plot_frame <- function() {
  for (i in 1:length(data_frames)) {
    image.plot(data_frames[[i]], col = heat.colors(100),
               main = paste("Iteracja", i),
               zlim = c(0, 1))
    Sys.sleep(0.05)
  }
}

# Uruchamiamy animację
ani.options(interval = 0.1)
saveGIF(plot_frame(), movie.name = "laplace_heat.gif", ani.width = 600, ani.height = 600)

# Wyświetlenie ostatniego wyniku
image.plot(data_frames[[length(data_frames)]], col = heat.colors(100),
           main = "Wynik końcowy", zlim = c(0, 1))