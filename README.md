# Análisis de Radioprotección para un Nanosatélite CubeSat 1U 🛰️🪐

Este repositorio alberga el código automatizado para un análisis de radioprotección utilizando TOPASMC en una geometría correspondiente a un CubeSat 1U. 
Este proyecto nació con el fin de encontrar una alternitativa estructural de bajo costo para la construcción de un Nanosatélite con componentes electrónicos COTS, y que su estructura preservara la adquisición de datos por el hardware, evitando daños por efectos de eventos únicos (SEE).

## Estructura del código 🗒️📂

- **CUBESAT:** gifs e imágenes extraídas directamente del programa SPENVIS de la ESA.
- **Dose:** contiene cada código con la geometría principal del cubesat que integra una sub-capa de cada material, el nombre se organiza de la siguiente manera `CubeSat_[Material].txt`.
- **Geometry:** Contiene la geometría estandarizada con los lineamientos del CubeSat 1U.
- **Results:** contiene los archivos de salida .csv de cada material de blindaje proporcionados por los códigos de la carpeta `Dose`.
- **Source:** contiene 

```
├── CUBESAT
│   ├── orbit_globe.gif
│   ├── orbit_map.gif
│   └── orbit_time.png
├── Dose
│   ├── CubeSat_Copper.txt
│   ├── CubeSat_Delrin.txt
│   ├── CubeSat_Epoxy.txt
│   ├── CubeSat_PLA.txt
│   └── CubeSat_Polyester.txt
├── Geometry
│   ├── Blindaje.txt
│   └── CubeSat_Geom.txt
├── README.md
├── Results
│   ├── Al6061
│   │   ├── Dose_Al6061.csv
│   │   └── EnergyDeposit_Al6061.csv
│   ├── Al7075
│   │   ├── Dose_Al7075.csv
│   │   └── EnergyDeposit_Al7075.csv
│   ├── AnodizedAl
│   │   ├── Dose_AnodizedAluminium.csv
│   │   └── EnergyDeposit_AnodizedAluminium.csv
│   ├── Copper
│   │   ├── Dose_Copper_EMI_Tape.csv
│   │   └── EnergyDeposit_Copper_EMI_Tape.csv
│   ├── Delrin
│   │   ├── Dose_Delrin_300ATB.csv
│   │   └── EnergyDeposit_Delrin_300ATB.csv
│   ├── Epoxy
│   │   ├── Dose_SP527_Glass_Epoxy.csv
│   │   └── EnergyDeposit_SP527_Glass_Epoxy.csv
│   ├── PLA
│   │   ├── Dose_PLA_3D_Print.csv
│   │   └── EnergyDeposit_PLA_3D_Print.csv
│   └── Polyester
│       ├── Dose_Copper_EMI_Tape.csv
│       └── EnergyDeposit_Copper_EMI_Tape.csv
└── Source
    ├── CubeSat_Source.txt
    └── Testeo
        ├── Geom2.txt
        └── Source2.txt
```

## Instrucciones de uso ☑️
Para compilar cada material implementado en cada geometría se deben seguir los siguientes pasos:

1. **PhaseSpace_Galactic:** El código que genera la fuente de rayos código se encuentra ubicado en la ruta `/home/popo21/REPOS/RADIOPROTECTION/Source/CubeSat_Source.txt`. La forma correcta para compilar código utilizando TOPASMC es la siguiente:

```
topas "nombre_del_archivo.txt"
```

de manera que, para generar nuestra fuente es necesario ejecutar los siguientes comandos en nuestra bash

```
cd /home/popo21/REPOS/RADIOPROTECTION/Source
topas CubeSat_Source.txt
```

2. **Calculo de Blindaje:** para ejecutar la geometría general del nanosatélite con la fuente `PhaseSpace_Galactic.*`, se debe copiar el resultado en la carpeta 
`/home/popo21/REPOS/RADIOPROTECTION/Geometry`, y posteriormente compilar la geometría con el cálculo ya implementado.

```
cd /home/popo21/REPOS/RADIOPROTECTION/Source
cp -- PhaseSpace_Galactic.* ../Geometry/
cd ../Geometry/
topas CubeSat_Geom.txt
```