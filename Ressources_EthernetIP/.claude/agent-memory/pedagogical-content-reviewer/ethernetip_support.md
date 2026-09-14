---
name: ethernetip-support
description: Notes on the EtherNet/IP BUT GEII reference document (structure, quality baseline, known-fixed technical point)
metadata:
  type: project
---

The document `Ressources_EthernetIP` (main.tex EthernetIP.tex, sources/*.tex) is a reference
handout (not a corrected TP) for BUT2/BUT3 GEII students designing an EtherNet/IP
scanner/adapter communication layer in an OO Codesys application. Reading order per main.tex:
introduction, architecture_reseau, modele_cip, messagerie, objets_assembly,
mise_en_oeuvre_codesys, mise_en_oeuvre_m340, checklist_conception, glossaire.

Overall technical quality is high: CIP model (class/instance/attribute/service), Scanner/Adapter
vs producteur/consommateur distinction, RPI, explicit/implicit messaging, standard CIP objects
(0x01/0x04/0x06/0xF5/0xF6) were all found accurate on review 2026-09-11 — no changes needed there.

Known-fixed technical error (2026-09-11): sources/mise_en_oeuvre_m340.tex originally claimed the
M340 CPU's integrated Ethernet port (BMX P34 2020/2030/2040) does EtherNet/IP scanning alongside
Modbus TCP. This is wrong — on the M340 range, EtherNet/IP scanning is provided by the dedicated
BMX NOE 0100/0110 communication module; the CPU's embedded port is limited to Modbus TCP,
FactoryCast web diagnostics, and Global Data. Corrected accordingly, including the
Codesys/Control Expert vocabulary correspondence table. If this section is revisited, double-check
against current Schneider documentation since EtherNet/IP scanner support depends on module
firmware version.

Style/quality baseline: French prose, UPSTIinfor/UPSTIidee/UPSTIwarning environments, cross-refs
via \ref{sec:...} are all consistent and correctly targeted — no broken refs found.
