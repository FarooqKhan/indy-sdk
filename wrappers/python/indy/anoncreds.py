from .libindy import do_call, create_cb

from typing import Optional
from ctypes import *

import logging


async def issuer_create_and_store_claim_def(wallet_handle: int,
                                            issuer_did: str,
                                            schema_json: str,
                                            signature_type: Optional[str],
                                            create_non_revoc: bool) -> str:
    """
    Create keys (both primary and revocation) for the given schema
    and signature type (currently only CL signature type is supported).
    Store the keys together with signature type and schema in a secure wallet as a claim definition.
    The claim definition in the wallet is identifying by a returned unique key.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param issuer_did: a DID of the issuer signing claim_def transaction to the Ledger
    :param schema_json: schema as a json
    :param signature_type: signature type (optional). Currently only 'CL' is supported.
    :param create_non_revoc: whether to request non-revocation claim.
    :return: claim definition json containing information about signature type, schema and issuer's public key.
            Unique number identifying the public key in the wallet
    """
    pass


async def issuer_create_and_store_revoc_reg(wallet_handle: int,
                                            issuer_did: str,
                                            schema_seq_no: int,
                                            max_claim_num: int) -> (str, str):
    """
    Create a new revocation registry for the given claim definition.
    Stores it in a secure wallet identifying by the returned key.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param issuer_did: a DID of the issuer signing revoc_reg transaction to the Ledger
    :param schema_seq_no: seq no of a schema transaction in Ledger
    :param max_claim_num: maximum number of claims the new registry can process.
    :return: Revoc registry json
        Unique number identifying the revocation registry in the wallet
    """
    pass


async def issuer_create_claim(wallet_handle: int,
                              claim_req_json: str,
                              claim_json: str,
                              revoc_reg_seq_no: int,
                              user_revoc_index: int) -> (str, str):
    """
    Signs a given claim for the given user by a given key (claim ef).
    The corresponding claim definition and revocation registry must be already created
    an stored into the wallet.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param claim_req_json: a claim request with a blinded secret
        from the user (returned by prover_create_and_store_claim_req).
        Also contains schema_seq_no and issuer_did
        Example:
        {
            "blinded_ms" : <blinded_master_secret>,
            "schema_seq_no" : <schema_seq_no>,
            "issuer_did" : <issuer_did>
        }
    :param claim_json: a claim containing attribute values for each of requested attribute names.
        Example:
        {
            "attr1" : ["value1", "value1_as_int"],
            "attr2" : ["value2", "value2_as_int"]
        }
    :param revoc_reg_seq_no: (Optional, pass -1 if revoc_reg_seq_no is absentee) seq no of a revocation
     registry transaction in Ledger
    :param user_revoc_index: index of a new user in the revocation registry
     (optional, pass -1 if user_revoc_index is absentee; default one is used if not provided)
    :return: Revocation registry update json with a newly issued claim
        Claim json containing issued claim, issuer_did, schema_seq_no, and revoc_reg_seq_no
        used for issuance
        {
            "claim": <see claim_json above>,
            "signature": <signature>,
            "revoc_reg_seq_no", string,
            "issuer_did", string,
            "schema_seq_no", string,
        }
    """
    pass


async def issuer_revoke_claim(wallet_handle: int,
                              revoc_reg_seq_no: int,
                              user_revoc_index: int) -> str:
    """
    Revokes a user identified by a revoc_id in a given revoc-registry.
    The corresponding claim definition and revocation registry must be already
    created an stored into the wallet.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param revoc_reg_seq_no: seq no of a revocation registry transaction in Ledger
    :param user_revoc_index: index of the user in the revocation registry
    :return: Revocation registry update json with a revoked claim
    """
    pass


async def prover_store_claim_offer(wallet_handle: int,
                                   claim_offer_json: str) -> None:
    """
    Stores a claim offer from the given issuer in a secure storage.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param claim_offer_json: claim offer as a json containing information about the issuer and a claim:
        {
            "issuer_did": string,
            "schema_seq_no": string
        }
    :return: None.
    """
    pass


async def prover_get_claim_offers(wallet_handle: int,
                                  filter_json: str) -> str:
    """
    Gets all stored claim offers (see prover_store_claim_offer).
    A filter can be specified to get claim offers for specific Issuer, claim_def or schema only.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param filter_json: optional filter to get claim offers for specific Issuer, claim_def or schema only only
        Each of the filters is optional and can be combines
            {
                "issuer_did": string,
                "schema_seq_no": string
            }
    :return: A json with a list of claim offers for the filter.
        {
            [{"issuer_did": string,
            "schema_seq_no": string}]
        }
    """
    pass


async def prover_create_master_secret(wallet_handle: int,
                                      master_secret_name: str) -> None:
    """
    Creates a master secret with a given name and stores it in the wallet.
    The name must be unique.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param master_secret_name: a new master secret name
    :return: None.
    """
    pass


async def prover_create_and_store_claim_req(wallet_handle: int,
                                            prover_did: str,
                                            claim_offer_json: str,
                                            claim_def_json: str,
                                            master_secret_name: str) -> str:
    """
    Creates a clam request json for the given claim offer and stores it in a secure wallet.
    The claim offer contains the information about Issuer (DID, schema_seq_no),
    and the schema (schema_seq_no).
    The method gets public key and schema from the ledger, stores them in a wallet,
    and creates a blinded master secret for a master secret identified by a provided name.
    The master secret identified by the name must be already stored in the secure wallet (see prover_create_master_secret)
    The blinded master secret is a part of the claim request.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param prover_did: a DID of the prover
    :param claim_offer_json: claim offer as a json containing information about the issuer and a claim:
        {
            "issuer_did": string,
            "schema_seq_no": string
        }
    :param claim_def_json: claim definition json associated with issuer_did and schema_seq_no in the claim_offer
    :param master_secret_name: the name of the master secret stored in the wallet
    :return: Claim request json.
        {
            "blinded_ms" : <blinded_master_secret>,
            "schema_seq_no" : <schema_seq_no>,
            "issuer_did" : <issuer_did>
        }
    """
    pass


async def prover_store_claim(wallet_handle: int,
                             claims_json: str) -> None:
    """
    Updates the claim by a master secret and stores in a secure wallet.
    The claim contains the information about
    schema_seq_no, issuer_did, revoc_reg_seq_no (see issuer_create_claim).
    Seq_no is a sequence number of the corresponding transaction in the ledger.
    The method loads a blinded secret for this key from the wallet,
    updates the claim and stores it in a wallet.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param claims_json: claim json:
        {
            "claim": {attr1:[value, value_as_int]}
            "signature": <signature>,
            "schema_seq_no": string,
            "revoc_reg_seq_no", string
            "issuer_did", string
        }
    :return: None.
    """
    pass


async def prover_get_claims(wallet_handle: int,
                            filter_json: str) -> str:
    """
    Gets human readable claims according to the filter.
    If filter is NULL, then all claims are returned.
    Claims can be filtered by Issuer, claim_def and/or Schema.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param filter_json: filter for claims
        {
            "issuer_did": string,
            "schema_seq_no": string
        }
    :return: claims json
        [{
            "claim_uuid": <string>,
            "attrs": [{"attr_name" : "attr_value"}],
            "schema_seq_no": string,
            "issuer_did": string,
            "revoc_reg_seq_no": string,
        }]
    """
    pass


async def prover_get_claims_for_proof_req(wallet_handle: int,
                                          proof_request_json: str) -> str:
    """
    Gets human readable claims matching the given proof request.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param proof_request_json: proof request json
        {
            "name": string,
            "version": string,
            "nonce": string,
            "requested_attr1_uuid": <attr_info>,
            "requested_attr2_uuid": <attr_info>,
            "requested_attr3_uuid": <attr_info>,
            "requested_predicate_1_uuid": <predicate_info>,
            "requested_predicate_2_uuid": <predicate_info>,
        }
    :return: json with claims for the given pool request.
        Claim consists of uuid, human-readable attributes (key-value map), schema_seq_no, issuer_did and revoc_reg_seq_no.
            {
                "requested_attr1_uuid": [claim1, claim2],
                "requested_attr2_uuid": [],
                "requested_attr3_uuid": [claim3],
                "requested_predicate_1_uuid": [claim1, claim3],
                "requested_predicate_2_uuid": [claim2],
            }, where claim is
            {
                "claim_uuid": <string>,
                "attrs": [{"attr_name" : "attr_value"}],
                "schema_seq_no": string,
                "issuer_did": string,
                "revoc_reg_seq_no": string,
            }
    """
    pass


async def prover_create_proof(wallet_handle: int,
                              proof_req_json: str,
                              requested_claims_json: str,
                              schemas_json: str,
                              master_secret_name: str,
                              claim_defs_json: str,
                              revoc_regs_json: str) -> str:
    """
    Creates a proof according to the given proof request
    Either a corresponding claim with optionally revealed attributes or self-attested attribute must be provided
    for each requested attribute (see indy_prover_get_claims_for_pool_req).
    A proof request may request multiple claims from different schemas and different issuers.
    All required schemas, public keys and revocation registries must be provided.
    The proof request also contains nonce.
    The proof contains either proof or self-attested attribute value for each requested attribute.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param proof_req_json: proof request json as come from the verifier
        {
            "nonce": string,
            "requested_attr1_uuid": <attr_info>,
            "requested_attr2_uuid": <attr_info>,
            "requested_attr3_uuid": <attr_info>,
            "requested_predicate_1_uuid": <predicate_info>,
            "requested_predicate_2_uuid": <predicate_info>,
        }
    :param requested_claims_json: either a claim or self-attested attribute for each requested attribute
        {
            "requested_attr1_uuid": [claim1_uuid_in_wallet, true <reveal_attr>],
            "requested_attr2_uuid": [self_attested_attribute],
            "requested_attr3_uuid": [claim2_seq_no_in_wallet, false]
            "requested_attr4_uuid": [claim2_seq_no_in_wallet, true]
            "requested_predicate_1_uuid": [claim2_seq_no_in_wallet],
            "requested_predicate_2_uuid": [claim3_seq_no_in_wallet],
        }
    :param schemas_json: all schema jsons participating in the proof request
        {
            "claim1_uuid_in_wallet": <schema1>,
            "claim2_uuid_in_wallet": <schema2>,
            "claim3_uuid_in_wallet": <schema3>,
        }
    :param master_secret_name: the name of the master secret stored in the wallet

    :param claim_defs_json: all claim definition jsons participating in the proof request
        {
            "claim1_uuid_in_wallet": <claim_def1>,
            "claim2_uuid_in_wallet": <claim_def2>,
            "claim3_uuid_in_wallet": <claim_def3>,
        }
    :param revoc_regs_json: all revocation registry jsons participating in the proof request
        {
            "claim1_uuid_in_wallet": <revoc_reg1>,
            "claim2_uuid_in_wallet": <revoc_reg2>,
            "claim3_uuid_in_wallet": <revoc_reg3>,
        }
    :return: Proof json
        For each requested attribute either a proof (with optionally revealed attribute value) or
        self-attested attribute value is provided.
        Each proof is associated with a claim and corresponding schema_seq_no, issuer_did and revoc_reg_seq_no.
        There ais also aggregated proof part common for all claim proofs.
            {
                "requested": {
                    "requested_attr1_id": [claim_proof1_uuid, revealed_attr1, revealed_attr1_as_int],
                    "requested_attr2_id": [self_attested_attribute],
                    "requested_attr3_id": [claim_proof2_uuid]
                    "requested_attr4_id": [claim_proof2_uuid, revealed_attr4, revealed_attr4_as_int],
                    "requested_predicate_1_uuid": [claim_proof2_uuid],
                    "requested_predicate_2_uuid": [claim_proof3_uuid],
                }
                "claim_proofs": {
                    "claim_proof1_uuid": [<claim_proof>, issuer_did, schema_seq_no, revoc_reg_seq_no],
                    "claim_proof2_uuid": [<claim_proof>, issuer_did, schema_seq_no, revoc_reg_seq_no],
                    "claim_proof3_uuid": [<claim_proof>, issuer_did, schema_seq_no, revoc_reg_seq_no]
                },
                "aggregated_proof": <aggregated_proof>
            }
    """
    pass


async def verifier_verify_proof(wallet_handle: int,
                                proof_request_json: str,
                                proof_json: str,
                                schemas_json: str,
                                claim_defs_jsons: str,
                                revoc_regs_json: str) -> bool:
    """
    Verifies a proof (of multiple claim).
    All required schemas, public keys and revocation registries must be provided.

    :param wallet_handle: wallet handler (created by open_wallet).
    :param proof_request_json: initial proof request as sent by the verifier
        {
            "nonce": string,
            "requested_attr1_uuid": <attr_info>,
            "requested_attr2_uuid": <attr_info>,
            "requested_attr3_uuid": <attr_info>,
            "requested_predicate_1_uuid": <predicate_info>,
            "requested_predicate_2_uuid": <predicate_info>,
        }
    :param proof_json: proof json
        For each requested attribute either a proof (with optionally revealed attribute value) or
        self-attested attribute value is provided.
        Each proof is associated with a claim and corresponding schema_seq_no, issuer_did and revoc_reg_seq_no.
        There ais also aggregated proof part common for all claim proofs.
            {
                "requested": {
                    "requested_attr1_id": [claim_proof1_uuid, revealed_attr1, revealed_attr1_as_int],
                    "requested_attr2_id": [self_attested_attribute],
                    "requested_attr3_id": [claim_proof2_uuid]
                    "requested_attr4_id": [claim_proof2_uuid, revealed_attr4, revealed_attr4_as_int],
                    "requested_predicate_1_uuid": [claim_proof2_uuid],
                    "requested_predicate_2_uuid": [claim_proof3_uuid],
                }
                "claim_proofs": {
                    "claim_proof1_uuid": [<claim_proof>, issuer_did, schema_seq_no, revoc_reg_seq_no],
                    "claim_proof2_uuid": [<claim_proof>, issuer_did, schema_seq_no, revoc_reg_seq_no],
                    "claim_proof3_uuid": [<claim_proof>, issuer_did, schema_seq_no, revoc_reg_seq_no]
                },
                "aggregated_proof": <aggregated_proof>
            }
    :param schemas_json: all schema jsons participating in the proof
        {
            "claim_proof1_uuid": <schema>,
            "claim_proof2_uuid": <schema>,
            "claim_proof3_uuid": <schema>
        }
    :param claim_defs_jsons: all claim definition jsons participating in the proof
        {
            "claim_proof1_uuid": <claim_def>,
            "claim_proof2_uuid": <claim_def>,
            "claim_proof3_uuid": <claim_def>
        }
    :param revoc_regs_json: all revocation registry jsons participating in the proof
        {
            "claim_proof1_uuid": <revoc_reg>,
            "claim_proof2_uuid": <revoc_reg>,
            "claim_proof3_uuid": <revoc_reg>
        }
    :return: valid: true - if signature is valid, false - otherwise
    """
    pass
