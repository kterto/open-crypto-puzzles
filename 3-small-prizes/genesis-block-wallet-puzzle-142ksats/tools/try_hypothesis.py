#!/usr/bin/env python3
"""
try_hypothesis.py -- test one idea about this puzzle by hand.

Purpose:
    The model is fixed: a 128-bit digest of some genesis data becomes the entropy of a
    12-word BIP39 mnemonic, a name is the passphrase, and two keys derived along BIP48 go
    into a 2-of-2 witness script whose SHA-256 is the escrow's witness program. What is not
    known is which part of the block is hashed, which digest function is used, and how the
    name is written. This script lets a person try one combination, or sweep the dimensions
    left unspecified, without editing any code.

    Anything not given is swept. Giving nothing sweeps everything, which is the big pass and
    takes hours; give at least a part or an input.

Usage (run from this folder):
    python3 tools/try_hypothesis.py --list
    python3 tools/try_hypothesis.py --part headline --form hex --digest md5 --passphrase "Hal Finney"
    python3 tools/try_hypothesis.py --part merkle_be --digest all --passphrase "Hal Finney"
    python3 tools/try_hypothesis.py --text "The Times 03/Jan/2009" --form raw --digest md5
    python3 tools/try_hypothesis.py --hex 4a5e1e4b --form dec --names
    python3 tools/try_hypothesis.py --entropy 5f4dcc3b5aa765d61d8327deb882cf99 --passphrase "Hal"
    python3 tools/try_hypothesis.py --part nonce --digest all --names --show
    python3 tools/try_hypothesis.py --selftest

Input:
    Command-line arguments. The genesis block is read from data/genesis-block.hex. No network.

Output:
    One line per candidate when --show is given, a progress count otherwise, then a verdict.
    MATCH prints the part, the form, the digest, the passphrase, the two derivation paths and
    the mnemonic, and exits 0. Exhausting the space without a match exits 1.

Dependencies: stdlib, bip_utils. Reuses oracle.py and check_digest_model.py from this folder.
"""

from __future__ import annotations

import argparse
import itertools
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import oracle  # noqa: E402
import check_digest_model as model  # noqa: E402

FORMS = ["raw", "hex", "HEX", "dec", "bin", "bin_nolead", "bin_spaced",
         "ascii", "ascii_dots", "dec_bytes", "dec_bytes_csv"]


def all_parts() -> dict[str, bytes]:
    parts = dict(model.PARTS)
    parts.update(model.coinbase_parts())
    return parts


def all_digests(blob: bytes) -> dict[str, bytes]:
    out = dict(model.digests(blob))
    try:
        out.update(model.extra_digests(blob))
    except Exception:
        pass
    return out


def resolve_input(args) -> list[tuple[str, bytes]]:
    if args.text is not None:
        return [("--text", args.text.encode())]
    if args.hex is not None:
        return [("--hex", bytes.fromhex(args.hex))]
    if args.file is not None:
        with open(args.file, "rb") as f:
            return [(os.path.basename(args.file), f.read())]
    parts = all_parts()
    if args.part:
        if args.part not in parts:
            sys.exit(f"unknown part {args.part!r}; run --list to see the names")
        return [(args.part, parts[args.part])]
    return sorted(parts.items())


def resolve_passphrases(args) -> list[str]:
    if args.passphrase:
        return list(args.passphrase)
    if args.names:
        return model.NAMES
    if args.wide_names:
        return model.NAMES_WIDE
    return model.NAMES


def resolve_paths(args):
    if args.path:
        return [(p, None) for p in args.path]
    return model.WAVE4_PATHS


def keys_for(mnemonic: str, passphrase: str, paths):
    from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
    ctx = Bip32Slip10Secp256k1.FromSeed(Bip39SeedGenerator(mnemonic).Generate(passphrase))
    out, nodes = [], {}
    for acct, suf in paths:
        try:
            node = nodes.get(acct)
            if node is None:
                node = nodes[acct] = ctx.DerivePath(acct)
            child = node if suf is None else node.DerivePath(suf)
            label = acct if suf is None else f"{acct}/{suf}"
            out.append((label, child.PublicKey().RawCompressed().ToBytes()))
            out.append((label + " (uncompressed)",
                        child.PublicKey().RawUncompressed().ToBytes()))
        except Exception:
            continue
    return out


def entropies_for(args) -> list[tuple[str, str, str, bytes]]:
    """(part, form, digest, entropy) for everything the arguments allow."""
    if args.entropy:
        raw = bytes.fromhex(args.entropy)
        if len(raw) != 16:
            sys.exit(f"--entropy needs 16 bytes (32 hex characters), got {len(raw)}")
        return [("--entropy", "-", "-", raw)]
    out = []
    forms = FORMS if args.form in (None, "all") else [args.form]
    for part, blob in resolve_input(args):
        rendered = model.four_forms(part, blob)
        for form in forms:
            key = f"{part}/{form}"
            if key not in rendered:
                continue
            digests = all_digests(rendered[key])
            names = digests.keys() if args.digest in (None, "all") else [args.digest]
            for dname in names:
                if dname not in digests:
                    sys.exit(f"unknown digest {dname!r}; run --list to see them")
                out.append((part, form, dname, digests[dname]))
    return out


def selftest() -> int:
    """The escrow must not match, and a known mnemonic must derive its published address."""
    from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip32Slip10Secp256k1
    ok = True
    m = str(Bip39MnemonicGenerator().FromEntropy(bytes(16)))
    expect = ("abandon abandon abandon abandon abandon abandon abandon abandon "
              "abandon abandon abandon about")
    print(f"zero entropy -> {m!r}: {'OK' if m == expect else 'FAIL'}")
    ok &= m == expect
    import hashlib
    seed = Bip39SeedGenerator(m).Generate("")
    pub = (Bip32Slip10Secp256k1.FromSeed(seed).DerivePath("m/84'/0'/0'/0/0")
           .PublicKey().RawCompressed().ToBytes())
    h160 = hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()
    addr = oracle.bech32_v0(h160)
    want = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"
    print(f"BIP84 vector -> {addr}: {'OK' if addr == want else 'FAIL'}")
    ok &= addr == want
    hit = oracle.check(oracle.REVEALED_A, oracle.REVEALED_B, oracle.TARGET_PROGRAM)
    print(f"negative control (revealed pair vs escrow): {'OK' if hit is None else 'FAIL'}")
    ok &= hit is None
    wit = oracle.program(oracle.witness_script(oracle.REVEALED_A, oracle.REVEALED_B))
    hit = oracle.check(oracle.REVEALED_A, oracle.REVEALED_B, wit)
    print(f"positive control (revealed pair vs its own program): {'OK' if hit else 'FAIL'}")
    ok &= bool(hit)
    print("SELFTEST OK" if ok else "SELFTEST FAILED")
    return 0 if ok else 2


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Try one hypothesis about the entropy input, the digest and the passphrase.")
    src = ap.add_argument_group("what gets hashed (pick one; default sweeps every known part)")
    src.add_argument("--part", help="a named genesis part, see --list")
    src.add_argument("--text", help="arbitrary text to hash")
    src.add_argument("--hex", help="arbitrary bytes, as hex")
    src.add_argument("--file", help="a file whose bytes get hashed")
    src.add_argument("--entropy", help="skip the hashing, give the 16-byte entropy as hex")
    ap.add_argument("--form", choices=FORMS + ["all"],
                    help="how the part is written before hashing (default: all)")
    ap.add_argument("--digest", help="digest name, or 'all' (default: all)")
    ap.add_argument("--passphrase", action="append",
                    help="the passphrase, repeatable (default: the 47 name formats)")
    ap.add_argument("--names", action="store_true", help="sweep the 47 name formats")
    ap.add_argument("--wide-names", action="store_true", help="sweep the 137 name formats")
    ap.add_argument("--path", action="append",
                    help="derivation path, repeatable (default: the 52 BIP48 paths)")
    ap.add_argument("--show", action="store_true",
                    help="print every mnemonic and its first address as it is tried")
    ap.add_argument("--list", action="store_true", help="list the parts, forms and digests")
    ap.add_argument("--selftest", action="store_true", help="check the derivation against vectors")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.list:
        parts = all_parts()
        print(f"parts ({len(parts)}):")
        for name, blob in sorted(parts.items()):
            print(f"  {name:<20} {len(blob):>3} bytes  {blob[:24].hex()}")
        print(f"\nforms ({len(FORMS)}): " + ", ".join(FORMS))
        names = sorted(all_digests(b"x").keys())
        print(f"\ndigests ({len(names)}): " + ", ".join(names))
        print(f"\nname formats: {len(model.NAMES)} with --names, "
              f"{len(model.NAMES_WIDE)} with --wide-names")
        print(f"paths: {len(model.WAVE4_PATHS)} BIP48 paths by default")
        return 0

    from bip_utils import Bip39MnemonicGenerator

    ents = entropies_for(args)
    pws = resolve_passphrases(args)
    paths = resolve_paths(args)
    total = len(ents) * len(pws)
    print(f"{len(ents)} entropies x {len(pws)} passphrases x {len(paths)} paths "
          f"(both key encodings), pairs inside each seed", flush=True)

    t0, tried, seen = time.time(), 0, 0
    for part, form, dname, ent in ents:
        mnemonic = str(Bip39MnemonicGenerator().FromEntropy(ent))
        for pw in pws:
            tried += 1
            keys = keys_for(mnemonic, pw, paths)
            if args.show:
                first = keys[0][1].hex() if keys else "-"
                print(f"  {part}/{form} {dname} pw={pw!r}\n    {mnemonic}\n    {first}")
            for (la, ka), (lb, kb) in itertools.permutations(keys, 2):
                seen += 1
                if oracle.check(ka, kb) is not None:
                    print()
                    print("MATCH")
                    print(f"  part       {part}")
                    print(f"  form       {form}")
                    print(f"  digest     {dname}")
                    print(f"  entropy    {ent.hex()}")
                    print(f"  mnemonic   {mnemonic}")
                    print(f"  passphrase {pw!r}")
                    print(f"  key A      {la}  {ka.hex()}")
                    print(f"  key B      {lb}  {kb.hex()}")
                    print()
                    print("Sweep the funds before telling anyone. Do not post the mnemonic.")
                    return 0
            if tried % 50 == 0:
                el = time.time() - t0
                print(f"  {tried}/{total} combinations, {seen:,} pairs, {el:.0f}s", flush=True)

    el = time.time() - t0
    print(f"NO MATCH after {tried} combinations and {seen:,} ordered pairs in {el:.0f}s")
    return 1


if __name__ == "__main__":
    sys.exit(main())
