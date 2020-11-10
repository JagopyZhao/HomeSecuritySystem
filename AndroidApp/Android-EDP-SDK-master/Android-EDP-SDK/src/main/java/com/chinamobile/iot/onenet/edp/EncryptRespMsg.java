/*
 * Copyright (c) 2016-2018. China Mobile Communications Corporation. All rights reserved.
 */

package com.chinamobile.iot.onenet.edp;

import com.chinamobile.iot.onenet.edp.toolbox.RSAUtils;

import java.io.IOException;

/**
 * Created by chenglei on 2015/12/29.
 */
public class EncryptRespMsg extends EdpMsg {

    private String encryptSecretKey;

    public EncryptRespMsg() {
        super(Common.MsgType.ENCRYPTRESP);
    }

    public static void printHexString(String hint, byte[] b) {
        System.out.print(hint);
        for (int i = 0; i < b.length; i++) {
            String hex = Integer.toHexString(b[i] & 0xFF);
            if (hex.length() == 1) {
                hex = '0' + hex;
            }
            System.out.print(hex.toUpperCase() + " ");
        }
        System.out.println("");
    }

    @Override
    public void unpackMsg(byte[] msgData) throws IOException {
        int dataLen = msgData.length;
        printHexString("msgData: ",msgData);
        System.out.println("dataLen: "+dataLen);
        if (dataLen < 2) {
            throw new IOException("packet size too short. size:" + dataLen);
        }
        int keyLen = Common.twoByteToLen(msgData[0], msgData[1]);
        System.out.println("keyLen: "+keyLen);
        if (dataLen >= keyLen + 2) {
            byte[] bytes = new byte[keyLen];
            System.arraycopy(msgData, 2, bytes, 0, keyLen);
            encryptSecretKey = RSAUtils.bcd2Str(bytes);
        }
    }

    public String getEncryptSecretKey() {
        return encryptSecretKey;
    }
}
