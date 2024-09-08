
# Comparación entre `code-examples.txt` y `code-examples-arreglado.txt`

Este documento detalla las diferencias entre el archivo de código proporcionado y su version corregida con el fin de que cumpla las reglas gramaticales describidas en el pdf, `code-examples.txt` (original) y `code-examples-arreglado.txt` (corregido).

## 1. Uso de parentesis en el condicional luego del if 

- **Original:** `if not(blocked?(left))`
- **Corregido:** if(not(isblocked?(left)))` con paréntesis como es descrito en el pdf.

## 2. Nombres de funciones y valores

### blocked?/isblocked?

- **Original:** `blocked?(left)`
- **Corregido:** `isblocked?(left)` con paréntesis adicionales en la condición.

### rooomForChips/roomForchips

- **Original:** `while not zero?(rooomForChips)` con un error en `rooomForChips` y while que no está definidio en el pdf.
- **Corregido:** `do (not (zero?(roomForChips)))` con el error corregido y cambio en la estructura del ciclo finalizando el bloque con "od" como es descrito en el pdf.

### repeat/rep

- **Original:** `repeat roomForChips times` repeat no está definidio en el pdf.
- **Corregido:** `do (not (zero?(roomForChips)))` cambio en la estructura de repeticion con rep finalizando el bloque con "per" como es descrito en el pdf.

### move/walk

- **Original en `goend()`:** `move(one)` pero move no esta definido en el pdf
- **Corregido en `goend()`:** `walk(one)` la funcion que mas se aproximaria teniendo en cuenta los parametros

## 3. Ajustes de sintaxis adicionales

Se añadio un ";" en al final de la linea 2 despues del "fi" debido a que la estructura de control if cuenta como una instruccion dentro del bloque como descrito en el pdf y se agregan palabras clave de finalizacion de estructuras de control como es "per" y "od"



