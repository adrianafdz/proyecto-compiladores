# Lenguaje de programación ALOOP

## Requerimientos:
- Libreria PLY

## Manual de usuario:
- Puedes encontrarlo en la siguiente liga [Manual de Usuario](https://docs.google.com/document/d/1rLIgtuoYGWiibsKG82S3ZxK-QLvmWhS3-Ir1rftCOUc/edit?usp=sharing).

## Demo de ejecución:
- Se encuentra dentro de la liga [Demo Aloop](https://youtu.be/6eIn2McpHL0).

## Información:
Dentro de este lenguaje de programación orientado a objetos se tienen los tipos de datos:
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
Durante esta semana se realizó la propuesta del lenguaje, desarrollando la gramática, type matching, diagramas de sintaxis y tokens. Se codificó la parte del lexer.

## Segundo Avance
Se codificó toda la parte del parser basado en la gramática propuesta.

## Tercer Avance
Se codificó lo relacionado a la generación de cuádruplos de expresiones y las clases para manejar el directorio de funciones, la tabla de variables, el cubo semántico y los cuádruplos.

## Cuarto Avance
Se implementó código para la semántica de variables y funciones y para el manejo de directorios. Se desarrolló la parte de generación de código intermedio para los estatutos if y while. También se comenzaron a utilizar direcciones virtuales.

## Quinto Avance
Se desarrolló la generación de código intermedio para el estatuto for, las funciones y la validación de parámetros. También se implementó el cálculo de recursos de las funciones y la generación de un archivo de código intermedio.
Se hizo un cambio en la gramática original. Hicimos la diferenciación de la declaración de arreglos y su indexación. Esto para poder hacer los cálculos correspondientes de la indexación y para limitar la declaración para que solo acepte números y no expresiones.

## Sexto Avance 
Se desarrolló e implementó la clase dimStructure para el manejo de arreglos y matrices. Se desarrolló la lógica para manejar valores de retorno y se dividieron las direcciones virtuales que se tenían antes para manejarlas por tipo. Se comenzó a desarrollar la máquina virtual.
Se hizo un cambio a la gramática para no permitir que dentro de las funciones se declaren objetos. Es decir, solo existen los objetos globales.

## Séptimo Avance 
Generación de código de arreglos. Se implementó la lógica para el manejo de objetos, herencia y apuntadores. Se modificó el cubo semántico para incluir apuntadores. Se desarrolló la generación de código para manejar variables dimensionadas. Para la máquina virtual se desarrolló lo relacionado a las expresiones y estatutos read y print.

## Octavo Avance
Se implementó la creación de archivos para almacenar información sobre los recursos y constantes. Se modificó la lógica para el manejo de valores de retorno y se mejoró la detección y mensajes de error.
Se modificó la gramática original para aceptar strings en las expresiones, para que las funciones to_number y to_string solo se acepten en una expresión y para que la función print acepte cero argumentos. Se crearon nuevos cuádruplos para el manejo de objetos y arreglos (OBJREF, MEMBER, OBJIND, STARR).