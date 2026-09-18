#!/usr/bin/env python3
"""
check_digest_model.py -- pass 4 and pass 5, the model the author described between
2026-09-14 and 2026-09-17.

Purpose:
    The author's answers of 2026-09-15 and 2026-09-16 state that the BIP39 entropy "isn't
    the raw 16 bytes" but "a 128-bit digest", and that the passphrase "is a name", the name
    of whoever received the first transaction, in a format that has to be found by brute
    force. This script enumerates that model and checks every ordered pair of keys it
    produces against the escrow's witness program, exactly, with no network access.

    Wave 1 (--wave 1) pairs keys inside one seed: one digest, one passphrase, two different
    BIP48 paths. Wave 2 (--wave 2) pairs keys across seeds at the same path: two different
    digests, one passphrase, which is the standard two-cosigner reading of "both keys are
    derived independently from Genesis". Wave 3 (--wave 3) changes the inputs rather than the
    pairing: it hashes what a person types instead of the canonical bytes (trailing newline,
    trailing period, collapsed spacing, case forms, eight ways of writing the date, the block
    as a hex file), widens the name formats to 137, and adds the one pairing waves 1 and 2 do
    not cover, two different formats of the same name under one entropy.

    The entropy candidates are 16-byte digests of genesis data under 18 digest readings
    (MD5, the 128-bit truncations of SHA-1, SHA-224, SHA-256, double SHA-256, SHA-512,
    RIPEMD-160, HASH160, SHA3-256, BLAKE2b, BLAKE2s and SHAKE-128) over 73 genesis inputs
    (the coinbase text, the headline, the scriptSig, the raw block, the header, the coinbase
    transaction, the public key, the merkle root and block hash in both byte orders, the
    address, the header integers, each also in lower and upper-case hex).

    The passphrase candidates are 47 name formats for Hal Finney, Harold Finney and Satoshi
    Nakamoto (spaced, joined, separated, initial, lower, upper and capitalized).

Usage (run from this folder):
    python3 tools/check_digest_model.py --count             # sizes only, no derivation
    python3 tools/check_digest_model.py --wave 1 [--procs 8]
    python3 tools/check_digest_model.py --wave 2 [--procs 8]
    python3 tools/check_digest_model.py --wave 3 [--procs 8]
    python3 tools/check_digest_model.py --wave 4 [--procs 8]

Input:
    data/genesis-block.hex and the constants below. No network.

Output:
    Progress lines, then one summary line: ordered pairs tested, rate, witness re-found
    count, escrow matches. Exit 0 on a match, 1 on a certified negative, 2 if the witness
    was not re-found (an uncertified run).

Witness:
    The 2-of-2 pair revealed in block 963,629 is inserted into three of the groups (first,
    middle, last) and its own witness program is a second target. A run that does not
    re-find it in every marked group is reported as uncertified.

Dependencies: stdlib, bip_utils. Reuses oracle.py from this folder.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
import time
from multiprocessing import Pool

FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(FOLDER, "tools"))

import oracle  # noqa: E402

WITNESS_PROGRAM = oracle.program(oracle.witness_script(oracle.REVEALED_A, oracle.REVEALED_B))
TARGETS = {oracle.TARGET_PROGRAM: "ESCROW", WITNESS_PROGRAM: "WITNESS"}

BLOCK = bytes.fromhex(open(os.path.join(FOLDER, "data", "genesis-block.hex")).read().split()[0])
HEADER = BLOCK[:80]
COINBASE_TX = BLOCK[81:]
T = b"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
J = b"Chancellor on brink of second bailout for banks"
S = bytes.fromhex("04ffff001d0104") + bytes([0x45]) + T
MERKLE_BE = bytes.fromhex("4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b")
HASH_BE = bytes.fromhex("000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f")
PUBKEY = bytes.fromhex(
    "04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb"
    "649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f")
ADDRESS = b"1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
NONCE, TIME, BITS, VERSION = 2083236893, 1231006505, 486604799, 1

ACCOUNTS = [0, 1, 2, 3, 50, 170, 285, 2009, 20090103, 3012009, 1231006505, 2083236893, 486604799]
SCRIPTS = [0, 1, 2]
SUFFIXES = [None, (0, 0), (0, 1), (1, 0)]

WAVE2_PATHS = []
for _a in ACCOUNTS:
    for _s in SCRIPTS:
        WAVE2_PATHS.append((f"m/48'/0'/{_a}'/{_s}'", "0/0"))
    WAVE2_PATHS.append((f"m/48'/0'/{_a}'/2'", "0/1"))
    WAVE2_PATHS.append((f"m/48'/0'/{_a}'/2'", "1/0"))


def inputs() -> dict[str, bytes]:
    out: dict[str, bytes] = {}

    def add(name, b):
        if b:
            out[name] = b

    for name, b in [("T", T), ("J", J), ("S", S), ("block", BLOCK), ("header", HEADER),
                    ("coinbase_tx", COINBASE_TX), ("pubkey", PUBKEY), ("pubkey_x", PUBKEY[1:33]),
                    ("merkle_be", MERKLE_BE), ("merkle_le", MERKLE_BE[::-1]),
                    ("hash_be", HASH_BE), ("hash_le", HASH_BE[::-1]),
                    ("prevhash", bytes(32)), ("address", ADDRESS)]:
        add(name, b)
        add(name + "_hex", b.hex().encode())
        add(name + "_HEX", b.hex().upper().encode())
    for name, b in [("T_lower", T.lower()), ("T_upper", T.upper()), ("J_lower", J.lower()),
                    ("J_upper", J.upper()), ("T_nospace", T.replace(b" ", b"")),
                    ("J_nospace", J.replace(b" ", b"")), ("T32", T[:32]), ("T16", T[:16]),
                    ("J32", J[:32]), ("times", b"The Times"),
                    ("times_date", b"The Times 03/Jan/2009")]:
        add(name, b)
    for name, v in [("nonce", NONCE), ("time", TIME), ("bits", BITS), ("version", VERSION),
                    ("height", 0), ("reward", 50)]:
        add(name + "_dec", str(v).encode())
        add(name + "_be4", v.to_bytes(4, "big"))
        add(name + "_le4", v.to_bytes(4, "little"))
    add("bits_hex", b"1d00ffff")
    add("date", b"03/Jan/2009")
    return out


def digests(x: bytes) -> dict[str, bytes]:
    sha256 = hashlib.sha256(x).digest()
    sha256d = hashlib.sha256(sha256).digest()
    sha1 = hashlib.sha1(x).digest()
    sha512 = hashlib.sha512(x).digest()
    out = {
        "md5": hashlib.md5(x).digest(),
        "sha256[:16]": sha256[:16], "sha256[16:]": sha256[16:],
        "sha256d[:16]": sha256d[:16], "sha256d[16:]": sha256d[16:],
        "sha1[:16]": sha1[:16], "sha1[4:]": sha1[4:],
        "sha512[:16]": sha512[:16], "sha512[48:]": sha512[48:],
        "blake2b16": hashlib.blake2b(x, digest_size=16).digest(),
        "blake2s[:16]": hashlib.blake2s(x).digest()[:16],
        "sha3_256[:16]": hashlib.sha3_256(x).digest()[:16],
        "shake128": hashlib.shake_128(x).digest(16),
        "sha224[:16]": hashlib.sha224(x).digest()[:16],
    }
    try:
        rmd = hashlib.new("ripemd160", x).digest()
        h160 = hashlib.new("ripemd160", sha256).digest()
        out["ripemd160[:16]"] = rmd[:16]
        out["ripemd160[4:]"] = rmd[4:]
        out["hash160[:16]"] = h160[:16]
        out["hash160[4:]"] = h160[4:]
    except ValueError:
        pass
    return out


WAVE3_DIGESTS = ["md5", "sha256[:16]", "sha256[16:]", "sha256d[:16]", "sha256d[16:]",
                 "sha1[:16]", "sha1[4:]", "sha512[:16]", "sha512[48:]", "blake2b16",
                 "blake2s[:16]", "sha3_256[:16]", "shake128", "sha224[:16]",
                 "ripemd160[:16]", "hash160[:16]"]

T_TEXT = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
J_TEXT = "Chancellor on brink of second bailout for banks"
D_TEXT = "The Times 03/Jan/2009"
DATE_FORMS = ["3/Jan/2009", "03/01/2009", "3/1/2009", "03-Jan-2009", "2009-01-03",
              "Jan/03/2009", "January 3, 2009", "03/Jan/09"]


def typed_variants() -> list[bytes]:
    """What a person types, rather than the canonical genesis bytes."""
    bases = [T_TEXT, J_TEXT, D_TEXT]
    for date in DATE_FORMS:
        bases.append(T_TEXT.replace("03/Jan/2009", date))
        bases.append(D_TEXT.replace("03/Jan/2009", date))
    out = set()
    for b in bases:
        for f in [b, b.lower(), b.upper(), b.title(), b.capitalize(),
                  b.replace(" ", ""), b.replace(" ", "_"), b.replace(" ", "-"),
                  " ".join(b.split()), b + ".", b + "!", b + " ", " " + b,
                  b + "\n", b + "\r\n", f'"{b}"', f"'{b}'"]:
            out.add(f.encode())
    for blob in (BLOCK.hex(), BLOCK.hex().upper()):
        out.add(blob.encode())
        out.add((blob + "\n").encode())
    out.add(BLOCK)
    out.add(HEADER)
    return sorted(out)


def wide_names() -> list[str]:
    out = []
    for first, last in [("Hal", "Finney"), ("Harold", "Finney"), ("Satoshi", "Nakamoto")]:
        for c in [f"{first} {last}", f"{last} {first}", first + last, last + first,
                  f"{first}_{last}", f"{first}-{last}", f"{first}.{last}",
                  f"{first[0]}{last}", f"{first[0]}. {last}", f"{first[0]}.{last}",
                  first, last, f"{first} {last} ", f" {first} {last}", f"{first}  {last}"]:
            out += [c, c.lower(), c.upper(), c.title()]
    out += ["Harold Thomas Finney II", "Harold T. Finney II", "Hal Finney (1956-2014)",
            "hal@finney.org", "halfinney", "HalFinney2009", "satoshin@gmx.com"]
    return list(dict.fromkeys(out))


def names() -> list[str]:
    out = []
    for first, last in [("Hal", "Finney"), ("Harold", "Finney"), ("Satoshi", "Nakamoto")]:
        full = f"{first} {last}"
        out += [full, full.lower(), full.upper(), first + last, (first + last).lower(),
                (first + last).upper(), first, first.lower(), last, last.lower(), last.upper(),
                f"{first}_{last}", f"{first}-{last}", f"{first.lower()}_{last.lower()}",
                f"{first.lower()}.{last.lower()}", f"{first[0]}{last}", f"{first[0]}. {last}"]
    out += ["Harold Thomas Finney II", "Hal", "finney", "satoshi", "Satoshi", "nakamoto"]
    return list(dict.fromkeys(out))


NAMES = names()


def entropies() -> list[tuple[bytes, str]]:
    ents: dict[bytes, str] = {}
    for iname, ib in inputs().items():
        for dname, d in digests(ib).items():
            ents.setdefault(d, f"{dname}({iname})")
    return list(ents.items())


ENTS = entropies()


def _wave1(job):
    from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip32Slip10Secp256k1
    label, entropy, marked = job
    mnemonic = str(Bip39MnemonicGenerator().FromEntropy(entropy))
    hits, npairs, wit = [], 0, 0
    for pw in NAMES:
        ctx = Bip32Slip10Secp256k1.FromSeed(Bip39SeedGenerator(mnemonic).Generate(pw))
        keys, paths = [], []
        for a in ACCOUNTS:
            for s in SCRIPTS:
                try:
                    node = ctx.DerivePath(f"m/48'/0'/{a}'/{s}'")
                except Exception:
                    continue
                for suf in SUFFIXES:
                    try:
                        n = node if suf is None else node.DerivePath(f"{suf[0]}/{suf[1]}")
                    except Exception:
                        continue
                    keys.append(n.PublicKey().RawCompressed().ToBytes())
                    paths.append(f"m/48'/0'/{a}'/{s}'" +
                                 ("" if suf is None else f"/{suf[0]}/{suf[1]}"))
        if marked:
            keys += [oracle.REVEALED_A, oracle.REVEALED_B]
            paths += ["WITNESS_A", "WITNESS_B"]
        for i, ka in enumerate(keys):
            pre = b"\x52\x21" + ka + b"\x21"
            for j, kb in enumerate(keys):
                if i == j:
                    continue
                npairs += 1
                found = TARGETS.get(hashlib.sha256(pre + kb + b"\x52\xae").digest())
                if found == "WITNESS":
                    wit += 1
                elif found:
                    hits.append((label, pw, paths[i], paths[j], ka.hex(), kb.hex(), mnemonic))
    return npairs, hits, wit


def _wave2(job):
    from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip32Slip10Secp256k1
    pw, marked = job
    cols = {p: [] for p in WAVE2_PATHS}
    labels = []
    for ent, label in ENTS:
        mnemonic = str(Bip39MnemonicGenerator().FromEntropy(ent))
        ctx = Bip32Slip10Secp256k1.FromSeed(Bip39SeedGenerator(mnemonic).Generate(pw))
        labels.append(label)
        nodes = {}
        for acct, suf in WAVE2_PATHS:
            try:
                if acct not in nodes:
                    nodes[acct] = ctx.DerivePath(acct)
                cols[(acct, suf)].append(nodes[acct].DerivePath(suf).PublicKey()
                                         .RawCompressed().ToBytes())
            except Exception:
                cols[(acct, suf)].append(None)
    hits, npairs, wit = [], 0, 0
    for path, col in cols.items():
        keys = [k for k in col if k]
        lab = [labels[i] for i, k in enumerate(col) if k]
        if marked:
            keys += [oracle.REVEALED_A, oracle.REVEALED_B]
            lab += ["WITNESS_A", "WITNESS_B"]
        for i, ka in enumerate(keys):
            pre = b"\x52\x21" + ka + b"\x21"
            for j, kb in enumerate(keys):
                if i == j:
                    continue
                npairs += 1
                found = TARGETS.get(hashlib.sha256(pre + kb + b"\x52\xae").digest())
                if found == "WITNESS":
                    wit += 1
                elif found:
                    hits.append((pw, f"{path[0]}/{path[1]}", lab[i], lab[j],
                                 ka.hex(), kb.hex()))
    return npairs, hits, wit


NAMES_WIDE = wide_names()
CORE_KEYS = ("halfinney", "finneyhal", "satoshinakamoto", "nakamotosatoshi",
             "hal", "finney", "satoshi", "nakamoto")
CORE_IDX = [i for i, n in enumerate(NAMES_WIDE)
            if n.lower().replace(" ", "").replace("_", "").replace("-", "").replace(".", "")
            in CORE_KEYS][:24]
WAVE3_PATHS = ([(f"m/48\'/0\'/{a}\'/2\'", s) for a in ACCOUNTS if a != 20090103
                for s in ("0/0", "0/1")] +
               [(f"m/48\'/0\'/{a}\'/1\'", "0/0") for a in ACCOUNTS if a != 20090103])


def _wave3_keys(mnemonic, pw):
    from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
    ctx = Bip32Slip10Secp256k1.FromSeed(Bip39SeedGenerator(mnemonic).Generate(pw))
    keys, nodes = [], {}
    for acct, suf in WAVE3_PATHS:
        try:
            if acct not in nodes:
                nodes[acct] = ctx.DerivePath(acct)
            keys.append(nodes[acct].DerivePath(suf).PublicKey().RawCompressed().ToBytes())
        except Exception:
            keys.append(None)
    return keys


def _pair(ks_a, ks_b, same):
    n, found = 0, []
    for i, ka in enumerate(ks_a):
        if not ka:
            continue
        pre = b"\x52\x21" + ka + b"\x21"
        for j, kb in enumerate(ks_b):
            if not kb or (same and i == j):
                continue
            n += 1
            t = TARGETS.get(hashlib.sha256(pre + kb + b"\x52\xae").digest())
            if t:
                found.append((t, i, j))
    return n, found


def _wave3(job):
    from bip_utils import Bip39MnemonicGenerator
    ent, label, marked = job
    mnemonic = str(Bip39MnemonicGenerator().FromEntropy(ent))
    npairs, hits, wit, cols = 0, [], 0, []
    for k, pw in enumerate(NAMES_WIDE):
        ks = _wave3_keys(mnemonic, pw)
        if marked and k == 0:
            ks = ks + [oracle.REVEALED_A, oracle.REVEALED_B]
        cols.append(ks)
        n, found = _pair(ks, ks, True)
        npairs += n
        for t, i, j in found:
            if t == "WITNESS":
                wit += 1
            else:
                hits.append(("A", label, pw, i, j, mnemonic))
    b_paths = len([1 for acct, _ in WAVE3_PATHS if acct.endswith("2'")])
    for ia, a in enumerate(CORE_IDX):
        for b in CORE_IDX[ia + 1:]:
            n, found = _pair(cols[a][:b_paths], cols[b][:b_paths], False)
            npairs += n
            for t, i, j in found:
                if t == "WITNESS":
                    wit += 1
                else:
                    hits.append(("B", label, f"{NAMES_WIDE[a]}|{NAMES_WIDE[b]}", i, j, mnemonic))
    return npairs, hits, wit


def wave3_entropies() -> list[tuple[bytes, str]]:
    ents: dict[bytes, str] = {}
    for blob in typed_variants():
        for dname, d in digests(blob).items():
            if dname in WAVE3_DIGESTS:
                ents.setdefault(d, f"{dname}({blob[:40]!r})")
    return list(ents.items())


PARTS = {
    "version": (VERSION).to_bytes(4, "big"), "version_le": (VERSION).to_bytes(4, "little"),
    "prevhash": bytes(32),
    "merkle_be": MERKLE_BE, "merkle_le": MERKLE_BE[::-1],
    "time": (TIME).to_bytes(4, "big"), "time_le": (TIME).to_bytes(4, "little"),
    "bits": (BITS).to_bytes(4, "big"), "bits_le": (BITS).to_bytes(4, "little"),
    "nonce": (NONCE).to_bytes(4, "big"), "nonce_le": (NONCE).to_bytes(4, "little"),
    "blockhash_be": HASH_BE, "blockhash_le": HASH_BE[::-1],
    "header": HEADER, "block": BLOCK, "coinbase_tx": COINBASE_TX,
    "coinbase_text": T, "headline": J, "scriptsig": S,
    "pubkey": PUBKEY, "pubkey_x": PUBKEY[1:33], "pubkey_y": PUBKEY[33:],
    "merkle16": MERKLE_BE[:16], "blockhash16": HASH_BE[:16],
    "reward": (50).to_bytes(4, "big"),
}

WAVE4_PATHS = ([(f"m/48\'/0\'/{a}\'/2\'", s) for a in ACCOUNTS for s in ("0/0", "0/1")] +
               [(f"m/48\'/0\'/{a}\'/1\'", "0/0") for a in ACCOUNTS] +
               [(f"m/48\'/0\'/{a}\'/0\'", "0/0") for a in ACCOUNTS])
WAVE4_B_IDX = [i for i, (acct, suf) in enumerate(WAVE4_PATHS)
               if acct.endswith("2'") and suf == "0/0"]


def four_forms(name: str, b: bytes) -> dict[str, bytes]:
    """binary, hex, decimal and ASCII: the four views the author names."""
    out = {}
    bits = "".join(format(x, "08b") for x in b)
    out[f"{name}/raw"] = b
    out[f"{name}/hex"] = b.hex().encode()
    out[f"{name}/HEX"] = b.hex().upper().encode()
    out[f"{name}/dec"] = str(int.from_bytes(b, "big")).encode()
    out[f"{name}/bin"] = bits.encode()
    out[f"{name}/bin_nolead"] = bits.lstrip("0").encode() or b"0"
    out[f"{name}/bin_spaced"] = " ".join(format(x, "08b") for x in b).encode()
    out[f"{name}/ascii"] = b.decode("latin-1").encode("latin-1")
    out[f"{name}/ascii_dots"] = "".join(chr(x) if 32 <= x < 127 else "." for x in b).encode()
    out[f"{name}/dec_bytes"] = " ".join(str(x) for x in b).encode()
    out[f"{name}/dec_bytes_csv"] = ",".join(str(x) for x in b).encode()
    return out


def wave4_entropies() -> list[tuple[bytes, str]]:
    forms = {}
    for name, blob in PARTS.items():
        forms.update(four_forms(name, blob))
    ents: dict[bytes, str] = {}
    for label, blob in forms.items():
        for dname, d in digests(blob).items():
            ents.setdefault(d, f"{dname}({label})")
    return list(ents.items())


WAVE4_ENTS = wave4_entropies()


def _wave4_keys(mnemonic, pw):
    from bip_utils import Bip39SeedGenerator, Bip32Slip10Secp256k1
    ctx = Bip32Slip10Secp256k1.FromSeed(Bip39SeedGenerator(mnemonic).Generate(pw))
    keys, nodes = [], {}
    for acct, suf in WAVE4_PATHS:
        try:
            if acct not in nodes:
                nodes[acct] = ctx.DerivePath(acct)
            keys.append(nodes[acct].DerivePath(suf).PublicKey().RawCompressed().ToBytes())
        except Exception:
            keys.append(None)
    return keys


def _wave4(job):
    """Phase A for one entropy, and the /0/0 keys this entropy contributes to phase B."""
    from bip_utils import Bip39MnemonicGenerator
    idx, marked = job
    ent, label = WAVE4_ENTS[idx]
    mnemonic = str(Bip39MnemonicGenerator().FromEntropy(ent))
    npairs, hits, wit, export = 0, [], 0, []
    for pw_i, pw in enumerate(NAMES):
        ks = _wave4_keys(mnemonic, pw)
        export.append([ks[i] for i in WAVE4_B_IDX])
        kk = [k for k in ks if k]
        if marked and pw_i == 0:
            kk = kk + [oracle.REVEALED_A, oracle.REVEALED_B]
        n, found = _pair(kk, kk, True)
        npairs += n
        for t, i, j in found:
            if t == "WITNESS":
                wit += 1
            else:
                hits.append((label, pw, i, j, mnemonic))
    return idx, npairs, hits, wit, export


def run_wave4(procs):
    print(f"parts {len(PARTS)}, entropies {len(WAVE4_ENTS)}, names {len(NAMES)}, "
          f"paths {len(WAVE4_PATHS)}, phase-B paths {len(WAVE4_B_IDX)}", flush=True)
    marks = {0, len(WAVE4_ENTS) // 2, len(WAVE4_ENTS) - 1}
    jobs = [(i, i in marks) for i in range(len(WAVE4_ENTS))]
    t0, total, wit, allhits, table = time.time(), 0, 0, [], {}
    with Pool(procs) as pool:
        for k, (idx, n, hits, w, export) in enumerate(
                pool.imap_unordered(_wave4, jobs, chunksize=1)):
            total += n
            wit += w
            table[idx] = export
            for h in hits:
                allhits.append(h)
                print("MATCH A", h, flush=True)
            if k % 200 == 0:
                el = time.time() - t0
                print(f"  phase A {k}/{len(jobs)}, {total:,} pairs, "
                      f"{int(total / max(el, 1)):,}/s, {el:.0f}s", flush=True)
    print(f"  phase A complete: {total:,} pairs, witness {wit}", flush=True)

    order = sorted(table)
    for pw_i, pw in enumerate(NAMES):
        for p in range(len(WAVE4_B_IDX)):
            col = [(i, table[i][pw_i][p]) for i in order if table[i][pw_i][p]]
            if pw_i == 0 and p == 0:
                col += [(-1, oracle.REVEALED_A), (-2, oracle.REVEALED_B)]
            keys = [k for _, k in col]
            n, found = _pair(keys, keys, True)
            total += n
            for t, i, j in found:
                if t == "WITNESS":
                    wit += 1
                else:
                    allhits.append((col[i][0], col[j][0], pw, WAVE4_PATHS[WAVE4_B_IDX[p]]))
                    print("MATCH B", allhits[-1], flush=True)
        el = time.time() - t0
        print(f"  phase B {pw_i + 1}/{len(NAMES)} passphrases, {total:,} pairs, "
              f"{int(total / max(el, 1)):,}/s, {el:.0f}s", flush=True)
    el = time.time() - t0
    print(f"done: {total:,} ordered pairs in {el:.0f}s ({int(total / el):,}/s)")
    print(f"witness re-found {wit} of 4 expected")
    print(f"escrow matches: {len(allhits)}")
    if allhits:
        return 0
    return 1 if wit == 4 else 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave", type=int, choices=(1, 2, 3, 4))
    ap.add_argument("--procs", type=int, default=8)
    ap.add_argument("--count", action="store_true")
    args = ap.parse_args()

    per_seed = len(ACCOUNTS) * len(SCRIPTS) * len(SUFFIXES)
    seeds = len(ENTS) * len(NAMES)
    if args.count or not args.wave:
        print(f"inputs {len(inputs())}, entropies {len(ENTS)}, passphrases {len(NAMES)}")
        print(f"wave 1: seeds {seeds:,}, keys {seeds * per_seed:,}, "
              f"ordered pairs {seeds * per_seed * (per_seed - 1):,}")
        n = len(ENTS)
        print(f"wave 2: keys {n * len(NAMES) * len(WAVE2_PATHS):,}, "
              f"ordered pairs {n * (n - 1) * len(NAMES) * len(WAVE2_PATHS):,}")
        e3, p3, c3 = len(wave3_entropies()), len(WAVE3_PATHS), len(CORE_IDX)
        b3 = len([1 for acct, _ in WAVE3_PATHS if acct.endswith("2'")])
        e4, p4, b4 = len(WAVE4_ENTS), len(WAVE4_PATHS), len(WAVE4_B_IDX)
        print(f"wave 4: parts {len(PARTS)}, entropies {e4}, paths {p4}, ordered pairs "
              f"{e4 * len(NAMES) * p4 * (p4 - 1) + len(NAMES) * b4 * e4 * (e4 - 1):,}")
        print(f"wave 3: typed inputs {len(typed_variants())}, entropies {e3}, "
              f"names {len(NAMES_WIDE)}, paths {p3}, ordered pairs "
              f"{e3 * len(NAMES_WIDE) * p3 * (p3 - 1) + e3 * (c3 * (c3 - 1) // 2) * b3 * b3:,}")
        return 0

    if args.wave == 4:
        return run_wave4(args.procs)

    if args.wave == 1:
        marks = {0, len(ENTS) // 2, len(ENTS) - 1}
        jobs = [(label, ent, i in marks) for i, (ent, label) in enumerate(ENTS)]
        fn, expected_wit = _wave1, 3 * len(NAMES)
    elif args.wave == 2:
        marks = {0, len(NAMES) // 2, len(NAMES) - 1}
        jobs = [(pw, i in marks) for i, pw in enumerate(NAMES)]
        fn, expected_wit = _wave2, 3 * len(WAVE2_PATHS)
    else:
        ents3 = wave3_entropies()
        marks = {0, len(ents3) // 2, len(ents3) - 1}
        jobs = [(ent, label, i in marks) for i, (ent, label) in enumerate(ents3)]
        fn, expected_wit = _wave3, 3

    t0, total, wit, allhits = time.time(), 0, 0, []
    with Pool(args.procs) as pool:
        for k, (npairs, hits, w) in enumerate(pool.imap_unordered(fn, jobs, chunksize=1)):
            total += npairs
            wit += w
            for h in hits:
                allhits.append(h)
                print("MATCH", h, flush=True)
            if k % 25 == 0:
                el = time.time() - t0
                print(f"  {k}/{len(jobs)} groups, {total:,} pairs, "
                      f"{int(total / max(el, 1)):,}/s, {el:.0f}s", flush=True)
    el = time.time() - t0
    print(f"done: {total:,} ordered pairs in {el:.0f}s ({int(total / el):,}/s)")
    print(f"witness re-found {wit} of {expected_wit} expected")
    print(f"escrow matches: {len(allhits)}")
    if allhits:
        return 0
    return 1 if wit == expected_wit else 2


if __name__ == "__main__":
    sys.exit(main())
