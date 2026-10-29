# BAS Library — Multi-Equipment Layout

This repository holds the building-automation (BAS / HVAC) control-program
library.  The original layout was a flat collection of program dumps, most of
them written for one specific unit (Chiller01, Chiller02, RTU01, VAV-102,
Ahu101, ChwP01, …).  That made it impossible to have more than one unit of a
type.

The restructure groups every program by **equipment type** and **instance**, so
the library can cover any number of units.

---

## Directory layout

```
BAS Library/
├── Equipment/                # per-piece-of-equipment, per-instance program sets
│   ├── AHU/
│   │   └── AHU01/            # copy a folder to add AHU02
│   │       ├── Calculations/
│   │       ├── Programs/
│   │       └── Config/
│   ├── VAV/
│   │   └── VAV-102/
│   ├── Chiller/
│   │   └── Chiller01/
│   ├── ChilledWater/
│   │   └── GlobalSystem/
│   ├── Pump/
│   │   ├── Primary/
│   │   └── Secondary/
│   ├── Boiler/
│   │   └── Boiler01/
│   ├── RTU/
│   │   └── RTU01/
│   ├── UnitVentilator/
│   │   └── UV01/
│   └── SmartX/
├── Shared/                   # equipment-agnostic program sets
│   ├── Functions/            # math / logic functions
│   ├── Sequences/            # generic SOO (night cycle, override, mode)
│   ├── Staging/              # staging / DX / lead-lag
│   ├── Controller/           # smart-stat / controller dumps
│   └── Utility/              # bin/dec, timing calcs
├── Common/                   # used by multiple equipment types
├── Libraries/                # zip snapshots (source of truth is Equipment/)
├── Data/                     # non-code artifacts (points, graphics, .msg)
├── Tools/                    # migration script + reports
└── README.md
```

### Adding a new piece of equipment (onboarding)

The pattern is one folder per instance:

1. **Copy an existing instance folder** (e.g. `Equipment/AHU/AHU01`) to make the
   new one, e.g. `Equipment/AHU/AHU02`.  All program files travel with it.
2. **Point the instance to its own points / graphics** in `Data/`.
3. **Edit register / point names** so each unit addresses a disjoint point
   range.  The control logic is unit-agnostic; only the point/register
   binding differs between instances.
4. Add any equipment-specific programs to
   `Equipment/<Type>/<NewInstance>/Programs/` (and
   `Calculations/` / `Config` if needed).
5. If the new program is generic, move it to `Shared/` or `Common/` instead.

### Naming conventions

- Program files are named for their function, e.g. `SaTmpSptCtrl.txt`,
  `ChlrLdLgPrg.txt`, `DualDuctDprCtrl.txt`.
- Instance tags: `AHU01`, `VAV-102`, `Chiller01`, `RTU01`, `UV01`.
- Tagged copies of the *same* function for different units carry a suffix,
  e.g. `SaTmpSptCtrl - AHU12.txt`, `SaFanSpdCtrl - MEC.txt`.

---

## What each equipment library contains

| Library | Contents (sample programs) |
|---|---|
| **AHU** | supply fan control, supply air temp setpoint, mixed air / RA / relief dampers, economizer, zone mode, PID, heating/valve command, VRF |
| **VAV** | dual-duct pressure, CFM calcs, supply-air temp, economizer / night cycle, damper / reheat control, occupancy-based CFM, temp setpoint |
| **Chiller** | alarm control, staging, lead-lag, change leads |
| **ChilledWater** | global system, CHW valve control, pump lead-lag (2/3 stage), pump fail test, valve enable |
| **Pump** | primary + secondary pump control, speed signal |
| **Boiler** | boiler rotation, setpoint, start/stop |
| **RTU** | Trane RTU programs (diagnostic, economizer, mirrors, occupancy, reset, fan control, supply-temp) |
| **UnitVentilator** | DX stage-1 cooling, HW valve with bypass damper, mixed air damper, ventilation fan, OAD error |
| **SmartX** | mode override, occupancy override programs |

---

## How this was verified

- **195 non-zip files** + **7 zips** = 202 tracked files, all moved and git-renamed
  into `Equipment/`, `Shared/`, `Libraries/`, `Data/`.
- No stray txt files left at the top level; the 7 zips are now snapshot copies in
  `Libraries/` (the source of truth is the `Equipment/` tree).
- Git history is preserved — every move is a `git mv`, so file history is intact.
- The migration script is `Tools/migrate_complete.py`; re-run it to reproduce the
  layout from the original commit state.
