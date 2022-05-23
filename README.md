# Lenguaje de programacion ALOOP

# Requerimientos:
- Libreria PLY

## Informacion:
Dentro de este lenguaje de programacion se tienen los tipos de datos:
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

Donde la declaración de clases es:
```
    type <id> : <id> {
		<declaración de variables>
		<declaración de funciones>
    }
```

La declaración de variables es:
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
