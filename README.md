# BAS / HVAC Control-Program Library

A building-automation (BAS / HVAC) control-program library, restructured into a
**multi-equipment layout**. It holds control-program text dumps, shared logic,
equipment instances, and supporting artifacts for a mix of HVAC control systems
(primarily Schneider Electric EcoStruxure Building Operation / Smart Stat, with
Trane SpaceLogic graphics/config and BACnet point-build data).

> This repository is a **text-based program dump** library (plus the ancillary
> artifacts that go with it). It is intended as the human- and machine-readable
> source of truth for a building's HVAC control logic — not as a compiled
> controller image. The `.xbk`, `.tgml`, `.xml`, `.zip`, `.msg`, and `.xlsx`
> files shown in git history are snapshots/archives of the original tooling and
> point data.

---

## What's inside

### `Equipment/` — per-piece-of-equipment, per-instance program sets

One folder per equipment type, containing one folder per instance. Control logic
is unit-agnostic; only the point/register binding differs between instances.

| Directory | Contents (examples) |
|---|---|
| `Equipment/AHU/AHU01/` | supply fan control, supply-air temp setpoint, mixed air / RA / relief dampers, economizer, PID, heating/valve command, VRF |
| `Equipment/Boiler/Boiler01/` | boiler rotation, setpoint, start/stop + SpaceLogic config |
| `Equipment/Chiller/Chiller01/` | alarm control, staging, lead-lag, change leads |
| `Equipment/ChilledWater/GlobalSystem/` | CHW valve control, global pumps (2/3 stage lead-lag), pump fail test, valve enable |
| `Equipment/Pump/Primary/` + `Pump/Secondary/` | primary & secondary pump control, speed signal |
| `Equipment/RTU/RTU01/` | Trane RTU programs (diagnostic, economizer, mirrors, occupancy, reset, fan control, supply-temp) |
| `Equipment/SmartX/Occupancy/` + `Equipment/SmartX/Sensors/` | mode override, occupancy override, SmartX stat mode values |
| `Equipment/UnitVentilator/UV01/` | DX stage-1 cooling, HW valve with bypass damper, mixed-air damper, ventilation fan, OAD error |
| `Equipment/VAV/VAV-102/` | dual-duct pressure, CFM calcs, supply-air temp, economizer/night cycle, damper/reheat control, occupancy CFM, temp setpoint |

### `Shared/` — equipment-agnostic program sets

| Directory | Contents |
|---|---|
| `Shared/Sequences/` | generic sequence sets; e.g. `Mode.txt` computes the multistate zone command (`UnitState` 0–5: Off / Heating / Cooling / Cooling+Dehum / Economizer / Fan Only) from occupancy, room conditions, and OA |
| `Shared/Functions/` | math / logic functions (PID loop, input filter, reset setpoint, dewpoint, enthalpy, median) |
| `Shared/Controller/` | smart-stat / controller dumps (Schneider Smart Stat, B3 & I2 Smart Sensor, HW valve control) |
| `Shared/Staging/` | staging / DX / lead-lag |
| `Shared/Utility/` | bin⇄dec, timing calcs, supply-temp prototypes |

### `Data/Graphics/` — graphics / drawing artifacts

`RTU01.tgml`, `Sample VAV.tgml`, `MP-C-18A DxStg1&HwVwithBypassDamper.xml`.

### `Libraries/` — dropped source dumps and snapshots

The original program dumps (flat, single-unit, vendor-named) as they were
migrated out of the legacy tooling — kept here as archives/history:

- `Program Text Dumps/` — the bulk of the migrated dumps (`.txt`), plus the
  `.xbk`/`.zip`/`.msg`/`.xlsx` artifacts they shipped in.
- `Secondary Chilled Water Pumping LdLg 2 stages` / `3 stages`,
  `Chiller Staging 2 Chillers`, `B3 VAV Programs`, `TraneRTU` — per-system
  snapshots.

> The **source of truth is `Equipment/`**. `Libraries/` holds the dropped
> originals for reference only; the active, restructured code lives under
> `Equipment/` and `Shared/`.

---

## Adding a new piece of equipment (onboarding)

The pattern is one folder per instance:

1. **Copy an existing instance folder** (e.g. `Equipment/AHU/AHU01`) to make the
   new one, e.g. `Equipment/AHU/AHU02`. All program files travel with it.
2. **Point the instance to its own points / graphics** in `Data/Graphics/` (and
   the relevant `.xbk`/`.xml`).
3. **Edit register / point names** so each unit addresses a disjoint point range.
   The control logic is unit-agnostic; only the binding differs.
4. Add any equipment-specific programs to
   `Equipment/<Type>/<NewInstance>/Programs/`, and `Calculations/` / `Config/`
   as needed.
5. If a new program is generic, move it to `Shared/` instead of duplicating it.

---

## Naming conventions

- Program files are named for their function, e.g. `SaTmpSptCtrl.txt`,
  `ChlrLdLgPrg.txt`, `DualDuctDprCtrl.txt`.
- Instance tags: `AHU01`, `VAV-102`, `Chiller01`, `RTU01`, `UV01`, `Boiler01`.
- Tagged copies of the *same* function for different units carry a suffix,
  e.g. `SaTmpSptCtrl - AHU12.txt`, `SaFanSpdCtrl - MEC.txt`.

---

## Multi-equipment layout principle

The original layout was a flat collection of program dumps (most written for one
specific unit), which made it impossible to have more than one unit of a type.
The restructure groups every program by **equipment type** and **instance**, so
the library can cover any number of units without duplication.

---

## How this was (re)structured

- Every file was `git mv`'d into the new layout, so file history is preserved.
- `Tools/migrate_complete.py` (present in the restructure commit) reproduces the
  layout from the original commit state.
- The current work in progress is the **mode refactoring**: normalizing the
  multistate zone command (`Mode.txt` → `UnitState` 0–5) handling and its call
  sites across the library so occupied/deadband/unoccupied states are uniform.

---

## Notes

- Program files are `.txt` SE scripts (EcoStruxure Building Operation /
  Schneider Smart Stat plain-text syntax). Syntax reference:
  *EcoStruxure Building Operation – Plain English and Script Difference Guide*
  (04-40002-01-en), Section 4 "Program Language Differences" (native wait:
  `Wait <seconds>` / `Delay`; no literal `CheckWait`; system constants
  `True`/`False`/`On`/`Off`; system variables `Date`, `Hour`, `Month`, `Year`).
- Source control is via git; each move is a rename so history stays intact.
- Binary artifacts in git history (`.xbk`, `.zip`, `.msg`, `.xlsx`, `.tgml` with
  binary content) are snapshots from the original toolchain and are not always
  regenerated here.

---

## Repository state

- Branch: `main` (tracking `origin/main`)
- HEAD: `<last commit>` — work in progress ('mode refactoring')
- Working tree: clean
- Remote: `https://github.com/bryaburg/BAS.git`
