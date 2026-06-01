# Steganografija

Prezentacija iz predmeta **Bezbednost u sistemima elektronskog poslovanja**.

## Struktura foldera

- `original_images/` - ulazne slike koje se koriste za skrivanje poruke
- `output_images/` - generisane stego slike i LSB prikazi

Skripte automatski čitaju ulaze iz `original_images/` kada fajl postoji tamo, a sve izlazne slike čuvaju u `output_images/`. Ako se slika još nalazi u root folderu projekta, skripte će je i dalje pronaći dok je ne premestite.

Steganografija je tehnika skrivanja tajnih poruka unutar običnih fajlova (slika, zvuka) tako da niko ne posumnja da poruka uopšte postoji.
