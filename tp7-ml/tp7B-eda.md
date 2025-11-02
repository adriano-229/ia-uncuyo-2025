
2)

a)
  inclinacion_peligrosa count percent
                  <int> <int>   <dbl>
1                     0 22666    88.8
2                     1  2863    11.2

b)
We’re basically asking: does the probability of dangerous inclination vary between sections?

# A tibble: 10 × 5
# Groups:   seccion [9]
   seccion nombre_seccion                       total peligrosos proporcion
     <int> <chr>                                <int>      <int>      <dbl>
 1       2 "Barrio Civico"                       2994        472     0.158 
 2       3 "Parque O'Higgins"                    2267        336     0.148 
 3       4 "Cuarta Este Á\u0081rea Fundacional"  3159        416     0.132 
 4       5 "Residencial Sur"                     4132        522     0.126 
 5       4 "Cuarta Oeste"                        3513        430     0.122 
 6       1 "Parque Central"                      2469        279     0.113 
 7       7 "Residencial Parque"                  1009         81     0.0803
 8       6 "Residencial Norte"                   5144        299     0.0581
 9       8 "Aeroparque"                           840         28     0.0333
10      11 "San Agustín"                            2          0     0     


c)

# A tibble: 10 × 4
   especie        total peligrosos proporcion
   <chr>          <int>      <int>      <dbl>
 1 Morera         10542       1953     0.185 
 2 Acacia SP        576         89     0.155 
 3 Aguaribay        218         24     0.110 
 4 Tipa              74          8     0.108 
 5 Jacarand         296         27     0.0912
 6 Pltano          2426        215     0.0886
 7 Paraiso         2311        203     0.0878
 8 Acacia visco      62          4     0.0645
 9 Caducifolio      366         22     0.0601
10 Fresno americ…  1106         56     0.0506

3)
a)
b)
now we split that same histogram by class to see if dangerous trees tend to have thicker or thinner trunks.

From a 10bin viz i see that from 10cm to 180cm the freq of safe is a pretty constant that has average at 1000 but for the unsafe ones there is like a normal distribution with it's peak at 140cm (260 freq) and the shoulders and the mu+/-1sd on 80cm and 200cm (both with aprox. 100 freq).

c)
Elijo en base al tamaño de las barras a ojo, sobre todo me en base al de 10bins

# Create categorical version of circ_tronco_cm
train_data <- train_data %>%
  mutate(
    circ_tronco_cm_cat = case_when(
      circ_tronco_cm < 10  ~ "bajo",
      circ_tronco_cm < 100 ~ "medio",
      circ_tronco_cm < 180 ~ "alto",
      TRUE                 ~ "muy_alto"
    )
  )


d)

   TP   TN   FP  FN
1 374 2826 2841 342
                  Predicho
Actual             Peligroso (1) No peligroso (0)
  Peligroso (1)              374             2841
  No peligroso (0)           342             2826

