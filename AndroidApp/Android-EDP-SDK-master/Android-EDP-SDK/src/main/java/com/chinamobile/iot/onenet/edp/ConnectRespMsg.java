/*
 * Copyright (c) 2016-2018. China Mobile Communications Corporation. All rights reserved.
 */

package com.chinamobile.iot.onenet.edp;

import android.text.TextUtils;

import com.chinamobile.iot.onenet.edp.toolbox.AESUtils;

import java.io.IOException;


public class ConnectRespMsg extends EdpMsg {
    private boolean hasLicenseCode;    //是否包含授权码
    private byte resCode;            //连接操作返回码
    private int licenseCodeLen;        //授权码长度
    private String licenseCode;        //授权码

    ConnectRespMsg() {
        super(Common.MsgType.CONNRESP);
        hasLicenseCode = false;
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

    /*
     * unpack connect responce msg
     * check if has license code ,decode licence code.
     * @param msgData packet
     * @see onenet.edp.EdpMsg#unpackMsg(byte[])
     * @throws IOException if packet size is exception
     */
    @Override
    public void unpackMsg(byte[] msgData)
            throws IOException {

        printHexString("unpackMsg_msgData_before: ",msgData);
        if (!TextUtils.isEmpty(getSecretKey())) {
            switch (getAlgorithm()) {

                // AES加密，加密模式ECB，填充方式ISO10126padding
                case Common.Algorithm.ALGORITHM_AES:
                    try {
                        msgData = AESUtils.decrypt(msgData, getSecretKey().getBytes());
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    break;

            }
        }

        printHexString("unpackMsg_msgData: ",msgData);

        int dataLen = msgData.length;
        //连接响应报文最小长度为2
        if (dataLen < 2) {
            throw new IOException("packet size too short. size:" + dataLen);
        }

        this.resCode = msgData[1];
        if (msgData[0] == 1) {
            this.hasLicenseCode = true;
            if (dataLen < 4) {
                throw new IOException("packet has license code but size too short. size:" + dataLen);
            }
            int licenseCodeLen = Common.twoByteToLen(msgData[2], msgData[3]);
            int dataRemain = dataLen - 4;
            if (dataRemain < licenseCodeLen) {
                throw new IOException("packet remain size shorter than license code size");
            }
            this.licenseCode = new String(msgData, 4, licenseCodeLen);
        } else {
            this.hasLicenseCode = false;
        }
    }

    public byte getResCode() {
        return this.resCode;
    }

    public boolean getHasLicenseCode() {
        return this.hasLicenseCode;
    }

    public int getLicenseCodeLen() {
        return this.licenseCodeLen;
    }

    public String getLicenseCode() {
        return this.licenseCode;
    }
}
