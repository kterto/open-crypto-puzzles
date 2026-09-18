# State of play, 2026-09-18

Where this puzzle stands after seven passes, what is settled, what is not, and what to do
next. Read this first when picking the folder up again; `tested.md` has the negatives in full
and `leads.md` has the ranked leads with their costs.

## What the author has established

Every line below is his own wording, from `../clues/author-posts.md`, with the date it was
paid for.

- The witness script is a 2-of-2 multisig. Both keys are required (2026-08-23).
- Both keys come from the same genesis field, with no hash between the field and the keys,
  and are derived independently (2026-08-24).
- The derivation rule is `root -> multisig -> mainnet -> genesis_data -> script_type`, which
  is the BIP48 level order, and `genesis_data` is the account number (2026-08-28, 2026-09-10).
- The root is the BIP32 master key of a 12-word BIP39 mnemonic, with a passphrase
  (2026-09-10, 2026-09-11).
- The entropy is not the raw 16 bytes; it is a 128-bit digest (2026-09-15, 2026-09-16).
- The passphrase is a name: whoever received the first transaction. Its format has to be
  brute-forced (2026-09-14, 2026-09-15, 2026-09-17).
- The words were generated from entropy, and the wallet was built with tools that support
  BIPs 32, 39 and 48 (2026-09-15, 2026-09-14).
- The genesis data can be viewed in binary, hex, decimal or ASCII, and a solver who works out
  which part carries the entropy should try all four forms (2026-09-17).
- Whether both cosigners share the words and the passphrase: "Perhaps" (2026-09-15).

## What he refuses

Which part of the block carries the entropy. Refused for free twice and at 10,000 sats on
2026-09-18: "Some part of the genesis block. The hints are meant to clarify the map, not hand
you the route." He sells facts about the form of the input, not the input.

He has offered the escrow's two public keys for 50,000 sats. That removes the pairing step
from a search but not the derivation, which is the larger half of the cost in this folder's
runs, so it buys about a factor of two and no information about the input.

## What has been ruled out

Seven passes, 612,296,708,118 ordered pairs, each certified by re-finding the 2-of-2 pair
revealed in block 963,629 at the head, middle and tail of the key set. Full scope in
`tested.md`; reproduce with `../tools/check_digest_model.py --wave N`.

| Axis | Covered |
|---|---|
| Input part | 25 header and block parts, 19 coinbase and script parts, 114 windows of the block and the text |
| Input form | 11 renderings of binary, hex, decimal and ASCII, plus the six filtered forms the BIP39 tool produces |
| Digest | 24 readings, including MD5, MD4, MD2, the SHA family truncations, Keccak-256, SM3, BLAKE2 and the RIPEMD truncations |
| Passphrase | 137 name formats for Hal Finney, Harold Finney and Satoshi Nakamoto |
| Path | 52 BIP48 paths, 13 genesis accounts, script types 0', 1', 2', suffixes /0/0, /0/1, /1/0 |
| Key encoding | compressed and uncompressed, in every pairing combination |
| Cosigner shape | both keys from one seed, from two entropies of one part, and under two name formats |

## What to do next

1. **Read the channel first.** `python3 ../../tools/check_escrows.py --slug
   genesis-block-wallet-puzzle-142ksats`, then the escrow's transactions on mempool.space. A
   new author message is a new constraint; a spend ends the puzzle. Other players buy answers
   and those answers are public, so the channel can move without anyone here paying.
2. **Buy the digest function, if buying anything.** 10,000 sats, 48 bytes:
   `128-bit digest: MD5? Or truncated SHA256? Which one?` It is the one fact of the model he
   has never been asked and never refused, and an answer divides any future sweep by 24. The
   category question was refused at the same price, so treat this as a plausible bet and not
   a safe one.
3. **The BIP39 tool's raw setting.** Its "raw" mnemonic length skips the hash and uses the
   typed bits directly. That contradicts "it's a 128-bit digest", which is why it was not run,
   but it is the last untried branch of the tool whose behaviour matches every other statement
   the author has made. Cheap.
4. **Filtered forms of the window parts.** Wave 7 filtered the 44 structural parts only; the
   114 windows of wave 5 were not put through the BIP39 tool's character filter. Mechanical,
   a few hours, falling prior.
5. **Try one idea by hand** with `../tools/try_hypothesis.py`: name a part, a form, a digest
   and a passphrase, and it derives and compares in about a second. `--list` prints what is
   available, `--selftest` checks the derivation against the BIP39 and BIP84 vectors.

## What would change the picture

A statement from the author naming the part, a public solve of another puzzle in this style,
or an idea about "genesis data" that is not a field, a window or a rendering of either. Seven
passes failing on progressively more contrived inputs is the shape of a wrong premise, not of
an unlucky enumeration, and the premise this folder cannot test for free is which part of the
block he means.
