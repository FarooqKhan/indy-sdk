//
//  LedgerUtils.m
//  libindy-demo
//
//  Created by Anastasia Tarasova on 05.06.17.
//  Copyright © 2017 Kirill Neznamov. All rights reserved.
//

#import "LedgerUtils.h"
#import <libindy/libindy.h>
#import "TestUtils.h"
#import "WalletUtils.h"

@implementation LedgerUtils

+ (LedgerUtils *)sharedInstance
{
    static LedgerUtils *instance = nil;
    static dispatch_once_t dispatch_once_block;
    
    dispatch_once(&dispatch_once_block, ^{
        instance = [LedgerUtils new];
    });
    
    return instance;
}


- (NSError *)signAndSubmitRequestWithPoolHandle:(IndyHandle)poolHandle
                                   walletHandle:(IndyHandle)walletHandle
                                   submitterDid:(NSString *)submitterDid
                                    requestJson:(NSString *)requestJson
                                outResponseJson:(NSString **)responseJson
{
    XCTestExpectation* completionExpectation = [[ XCTestExpectation alloc] initWithDescription: @"completion finished"];
    __block NSError *err = nil;
    __block NSString *outJson = nil;
    NSError *ret;

    ret = [IndyLedger signAndSubmitRequestWithWalletHandle:walletHandle
                                                  poolHandle:poolHandle
                                                submitterDID:submitterDid
                                                 requestJSON:requestJson
                                                  completion:^(NSError* error, NSString *resultJson)
    {
        err = error;
        outJson = resultJson;
        [completionExpectation fulfill];
    }];
    
    if( ret.code != Success)
    {
        return ret;
    }
    
    [self waitForExpectations: @[completionExpectation] timeout:[TestUtils defaultTimeout]];
    
    if (responseJson){ *responseJson = outJson; }
    
    return err;
}

// MARK: Build nym request

- (NSError *) buildNymRequestWithSubmitterDid:(NSString*) submitterDid
                                    targetDid:(NSString*) targetDid
                                       verkey:(NSString*) verkey
                                        alias:(NSString*) alias
                                         role:(NSString*) role
                                   outRequest:(NSString**)resultJson;
{
    XCTestExpectation* completionExpectation = [[ XCTestExpectation alloc] initWithDescription: @"completion finished"];
    __block NSError *err = nil;
    __block NSString *outJson = nil;
    NSError *ret;
    
    ret = [IndyLedger buildNymRequestWithSubmitterDid:submitterDid
                                              targetDID:targetDid
                                                 verkey:verkey
                                                  alias:alias
                                                   role:role
                                             completion:^(NSError *error, NSString *json)
           {
               err = error;
               outJson = json;
               [completionExpectation fulfill];
           }];
    
    [self waitForExpectations: @[completionExpectation] timeout:[TestUtils longTimeout]];
    
    if( ret.code != Success)
    {
        return ret;
    }
    
    if (resultJson){ *resultJson = outJson; }
    
    return err;
}


- (NSError *) buildGetNymRequestWithSubmitterDid:(NSString *)submitterDid
                                       targetDid:(NSString *)targetDid
                                      outRequest:(NSString **)requestJson;
{
    XCTestExpectation* completionExpectation = [[ XCTestExpectation alloc] initWithDescription: @"completion finished"];
    __block NSError *err = nil;
    __block NSString *outJson = nil;
    NSError *ret;
    
    ret = [IndyLedger buildGetNymRequestWithSubmitterDid:submitterDid
                                                 targetDID:targetDid
                                                completion:^(NSError *error, NSString *json)
    {
        err = error;
        outJson = json;
        [completionExpectation fulfill];
    }];
    
    if( ret.code != Success)
    {
        return ret;
    }
    
    [self waitForExpectations: @[completionExpectation] timeout:[TestUtils longTimeout]];
    
    if (requestJson){ *requestJson = outJson; }
    
    return err;
}

// MARK: Build Attribute request

- (NSError *)buildAttribRequestWithSubmitterDid:(NSString *)submitterDid
                                      targetDid:(NSString *)targetDid
                                           hash:(NSString *)hash
                                            raw:(NSString *)raw
                                            enc:(NSString *)enc
                                     resultJson:(NSString **)resultJson
{
    XCTestExpectation* completionExpectation = [[ XCTestExpectation alloc] initWithDescription: @"completion finished"];
    __block NSError *err = nil;
    __block NSString *outJson = nil;
    NSError *ret;
    
    ret = [IndyLedger buildAttribRequestWithSubmitterDid:submitterDid
                                                 targetDID:targetDid
                                                      hash:hash
                                                       raw:raw
                                                       enc:enc
                                                completion:^(NSError* error, NSString* requestJson)
           {
               err = error;
               outJson = requestJson;
               [completionExpectation fulfill];
           }];
    
    if( ret.code != Success)
    {
        return ret;
    }
    
    [self waitForExpectations: @[completionExpectation] timeout:[TestUtils longTimeout]];
    
    if (resultJson){ *resultJson = outJson; }
    return err;
}


- (NSError *)buildGetAttribRequestWithSubmitterDid:(NSString *)submitterDid
                                         targetDid:(NSString *)targetDid
                                              data:(NSString *)data
                                        resultJson:(NSString **)resultJson
{
    XCTestExpectation* completionExpectation = [[ XCTestExpectation alloc] initWithDescription: @"completion finished"];
    __block NSError *err = nil;
    __block NSString *outRequest = nil;
    NSError *ret;
    
    ret = [IndyLedger buildGetAttribRequestWithSubmitterDid:submitterDid
                                                    targetDID:targetDid
                                                         data:data
                                                   completion:^(NSError *error, NSString *request)
    {
        err = error;
        outRequest = request;
        [completionExpectation fulfill];
    }];
    
    if( ret.code != Success)
    {
        return ret;
    }
    
    [self waitForExpectations: @[completionExpectation] timeout:[TestUtils longTimeout]];
    
    if (resultJson){ *resultJson = outRequest; }
    return err;
}
// MARK: Build schema request

- (NSError *)buildSchemaRequestWithSubmitterDid:(NSString *)submitterDid
                                           data:(NSString *)data
                                     resultJson:(NSString **)resultJson
{
    XCTestExpectation* completionExpectation = [[ XCTestExpectation alloc] initWithDescription: @"completion finished"];
    __block NSError *err = nil;
    __block NSString *result = nil;
    NSError *ret;
    
    ret = [IndyLedger buildSchemaRequestWithSubmitterDid:submitterDid
                                                      data:data
                                                completion:^(NSError *error, NSString *request)
           {
               err = error;
               result = request;
               [completionExpectation fulfill];
           }];
    
    if( ret.code != Success)
    {
        return ret;
    }

    [self waitForExpectations: @[completionExpectation] timeout:[TestUtils longTimeout]];
    
    if (resultJson){ *resultJson = result; }
    return err;
}

- (NSError *)buildGetSchemaRequestWithSubmitterDid:(NSString *)submitterDid
                                              dest:(NSString *)dest
                                              data:(NSString *)data
                                        resultJson:(NSString **)resultJson
{
    XCTestExpectation* completionExpectation = [[ XCTestExpectation alloc] initWithDescription: @"completion finished"];
    __block NSError *err = nil;
    __block NSString *result = nil;
    NSError *ret;
    
    
    ret = [IndyLedger buildGetSchemaRequestWithSubmitterDid:submitterDid
                                                         dest:dest
                                                         data:data
                                                   completion:^(NSError *error, NSString *request)
           {
               err = error;
               result = request;
               [completionExpectation fulfill];
           }];
    
    if( ret.code != Success)
    {
        return ret;
    }
    
    [self waitForExpectations: @[completionExpectation] timeout:[TestUtils longTimeout]];
    
    if (resultJson){ *resultJson = result; }
    return err;
}

// MARK: Build Node request

- (NSError *)buildNodeRequestWithSubmitterDid:(NSString *) submitterDid
                                    targetDid:(NSString *) targetDid
                                         data:(NSString *) data
                                   resultJson:(NSString **) resultJson
{
    XCTestExpectation* completionExpectation = [[ XCTestExpectation alloc] initWithDescription: @"completion finished"];
    __block NSError *err = nil;
    __block NSString *result = nil;
    NSError *ret;
    
    ret = [IndyLedger buildNodeRequestWithSubmitterDid:submitterDid
                                               targetDid:targetDid
                                                    data:data
                                              completion:^(NSError *error, NSString *request)
           {
               err = error;
               result = request;
               [completionExpectation fulfill];
           }];
    
    if( ret.code != Success)
    {
        return ret;
    }
    
    [self waitForExpectations: @[completionExpectation] timeout:[TestUtils longTimeout]];
    
    if (resultJson){ *resultJson = result; }
    return err;
}

// MARK: Build claim definition txn

- (NSError *)buildClaimDefTxnWithSubmitterDid:(NSString *) submitterDid
                                         xref:(NSString *) xref
                                signatureType:(NSString *) signatureType
                                         data:(NSString *) data
                                   resultJson:(NSString**) resultJson
{
    XCTestExpectation* completionExpectation = [[ XCTestExpectation alloc] initWithDescription: @"completion finished"];
    __block NSError *err = nil;
    __block NSString *result = nil;
    NSError *ret;
    
    ret = [IndyLedger buildClaimDefTxnWithSubmitterDid:submitterDid
                                                    xref:xref
                                           signatureType:signatureType
                                                    data:data
                                              completion:^(NSError* error, NSString* request)
           {
               err = error;
               result = request;
               [completionExpectation fulfill];
           }];
    
    if( ret.code != Success)
    {
        return ret;
    }
    
    [self waitForExpectations: @[completionExpectation] timeout:[TestUtils longTimeout]];
    
    if (resultJson){ *resultJson = result; }
    return err;
}

- (NSError *)buildGetClaimDefTxnWithSubmitterDid:(NSString *) submitterDid
                                            xref:(NSString *) xref
                                   signatureType:(NSString *) signatureType
                                          origin:(NSString *) origin
                                      resultJson:(NSString**) resultJson
{
    XCTestExpectation* completionExpectation = [[ XCTestExpectation alloc] initWithDescription: @"completion finished"];
    __block NSError *err = nil;
    __block NSString *result = nil;
    NSError *ret;
    
    ret = [IndyLedger buildGetClaimDefTxnWithSubmitterDid:submitterDid
                                                       xref:xref
                                              signatureType:signatureType
                                                     origin:origin
                                                 completion:^(NSError* error, NSString* request)
           {
               err = error;
               result = request;
               [completionExpectation fulfill];
           }];
    
    if( ret.code != Success)
    {
        return ret;
    }
    
    [self waitForExpectations: @[completionExpectation] timeout:[TestUtils longTimeout]];
    
    if (resultJson){ *resultJson = result; }
    return err;
}

- (NSError *)buildGetTxnRequestWithSubmitterDid:(NSString *)submitterDid
                                           data:(NSNumber *)data
                                     resultJson:(NSString**)resultJson
{
    XCTestExpectation* completionExpectation = [[ XCTestExpectation alloc] initWithDescription: @"completion finished"];
    __block NSError *err = nil;
    __block NSString *result = nil;
    NSError *ret;
    
    ret = [IndyLedger buildGetTxnRequestWithSubmitterDid:submitterDid
                                                      data:data
                                                completion:^(NSError* error, NSString* request)
           {
               err = error;
               result = request;
               [completionExpectation fulfill];
           }];
    
    if( ret.code != Success)
    {
        return ret;
    }
    
    [self waitForExpectations: @[completionExpectation] timeout:[TestUtils longTimeout]];
    
    if (resultJson) { *resultJson = result;}
    return err;
}
@end
