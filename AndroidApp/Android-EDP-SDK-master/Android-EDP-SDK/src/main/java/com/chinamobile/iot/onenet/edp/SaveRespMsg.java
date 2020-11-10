/*
 * Copyright (c) 2016-2018. China Mobile Communications Corporation. All rights reserved.
 */

package com.chinamobile.iot.onenet.edp;

import android.text.TextUtils;

import com.chinamobile.iot.onenet.edp.toolbox.AESUtils;

import java.io.IOException;

public class SaveRespMsg extends EdpMsg {
    private boolean hasResp;
    private int dataLength;
    private byte[] data;

    public SaveRespMsg() {
        super(Common.MsgType.SAVERESP);
    }

    @Override
    public void unpackMsg(byte[] msgData)
            throws IOException {

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

        int dataLen = msgData.length;
        if (msgData[0] == (byte) 0x80) {
            hasResp = true;
        } else {
            hasResp = false;
        }

        int dataRemain = dataLen - 1;
        if (dataRemain < 2) {
            throw new IOException("[sava_resp] data too short. dataLen=" + dataLen);
        }
        int respDataLen = Common.twoByteToLen(msgData[1], msgData[2]);
        dataRemain = dataRemain - 2;
        if (respDataLen > dataRemain) {
            throw new IOException("[save_resp] resp_data too long. respDataLen="
                    + respDataLen + " dataRemain=" + dataRemain);
        }
        data = new byte[respDataLen];
        System.arraycopy(msgData, 3, data, 0, respDataLen);
    }

    public boolean getHasResp() {
        return this.hasResp;
    }

    public int getDataLength() {
        return this.dataLength;
    }

    public byte[] getData() {
        return this.data;
    }
}
