# Lenguaje de programacion ALOOP

# Requerimientos:
- Libreria PLY

## Informacion:
Dentro de este lenguaje de programacion orientado a objetos se tienen los tipos de datos:
- number
- string
- objeto

La estructura del programa es:
```
    program <id>;
    <Declaración de clases>
    <Declaración de variables globales>
    <Declaración de funciones>

    # comentario
    main() {
        <estatutos>
    }
    end;
```

Donde la declaración de variables es:
```
    def <tipo><dimension> : <lista_ident>;
```

La declaración de funciones es:
```
    func <id> ( <params> ) : <tipo_func> {
		<Declaración de variables>
		<estatutos>
    }
```

La declaración de clases es:
```
    type <identificador> {
        <declaración de variables>
        <declaración de funciones>
    }
```

Para declarar una clase que hereda los atributos y métodos de otra, se utiliza la siguiente sintaxis:
```
    type <identificador_hijo> : <identificador_padre> {
        <declaración de variables>
        <declaración de funciones>
    }
```

Para declarar una variable que sea una instancia de una clase, se utiliza la siguiente sintaxis:
```
    def <identificador_clase> : <lista_identificadores> ;
```

Para acceder a un atributo de un objeto, se utiliza la siguiente sintaxis:
```
    <identificador_objeto>:<identificador_atributo> ;
```

De manera similar, para llamar a un método de una clase la sintaxis es:
```
    call <identificador_objeto>:<identificador_metodo>(<argumentos>) ;
```


## Primer Avance
Análisis Léxico y Sintáctico.

## Segundo Avance
Tabla de Variables y Cubo Semántico.

## Tercer Avance
Generación de código de expresiones y estatutos secuenciales.

## Cuarto Avance
Generación de código para condicionales (if-else) y bucles (while).

## Quinto Avance
Generación de cuádruplos del bucle for, generación de cuádruplos de funciones, uso de direcciones virtuales, validación de parámetros y argumentos

## Sexto Avance 
Generación de cuádruplos para arreglos de una y dos dimensiones, generación de máquina virtual.

## Séptimo Avance 
Se realizaron unos ajustes dentro de los parámetros y objetos en el compilador y se añadieron funciones a la Máquina Virtual.

## Octavo Avance
Se generaron archivos .json para los recursos y las constantes y que la máquina virtual pueda acceder a ellos, la funcionalidad de la máquina virtual y el primer avance de la documentación final la cual incluye el Manual de Usuario