
//mui初始化
mui.init();

var api = new OneNetApi('GPbHpXhSCwlYyIxfdxoMpcAYJKY=');

var dataObj;
/**
 * 读取设备多个数据流
 * api.getDataStreams(设备id)
 * */
 function getDataStrFromOneNet(){
	api.getDataStreams(559451901).done(function(data){
		if(data.error === 'succ'){
			
			for (i = 0; i < 9; i++) { 
				var atPoint = data.data[i]["id"];
				var valuePoint = data.data[i]["current_value"];
				if(atPoint === "humi"){
					$(".humi").empty;
					$(".humi").text(valuePoint);
					if(valuePoint > 90){
						mui.alert('The humidity is too high. Be careful!','AlarmInfo','got it');
					}
				}else if(atPoint === "temp"){
					$(".temp").empty;
					$(".temp").text(valuePoint);
					if(valuePoint > 50){
						mui.alert('The temperature is too high. Be careful!','AlarmInfo','got it');
					}
				}else if(atPoint === "gas"){
					$(".gas").empty;
					if(data.data[i]["current_value"] === 0){
						$(".gas").text("closed");
					}else{
						$(".gas").text("triggered");
						mui.alert('Gas is triggered. Be careful!','AlarmInfo','got it');
					}
				}else if(atPoint === "motion"){
					$(".motion").empty;
					if(data.data[i]["current_value"] === 0){
						$(".motion").text("closed");
					}else{
						$(".motion").text("triggered");
						mui.alert('Motion is triggered. Be careful!','AlarmInfo','got it');
					}
				}else if(atPoint === "fire"){
					$(".fire").empty;
					if(data.data[i]["current_value"] === 0){
						$(".fire").text("closed");
					}else{
						$(".fire").text("triggered");
						mui.alert('Fire is triggered. Be careful!','AlarmInfo','got it');
					}
				}else if(atPoint === "soil"){
					$(".soil").empty;
					if(data.data[i]["current_value"] === 0){
						$(".soil").text("closed");
					}else{
						$(".soil").text("triggered");
						mui.alert('Soil is triggered. Be careful!','AlarmInfo','got it');
					}
				}else if(atPoint === "rain"){
					$(".rain").empty;
					if(data.data[i]["current_value"] === 0){
						$(".rain").text("closed");
					}else{
						$(".rain").text("triggered");
						mui.alert('Rain is triggered. Be careful!','AlarmInfo','got it');
					}
				}else if(atPoint === "relay"){
					$(".relay").empty;
					if(data.data[i]["current_value"] === 0){
						$(".relay").text("closed");
					}else{
						$(".relay").text("opened");
					}
				}else if(atPoint === "motor"){
					$(".motor").empty;
					if(data.data[i]["current_value"] === 0){
						$(".motor").text("closed");
					}else{
						$(".motor").text("opened");
					}
				}else{
					mui.toast("Parameter Error!");
				}
			}
			// mui.toast("Updated");
		}else{
			mui.toast("Update Failed");
		}
	});
 }

/**
 * 获取数据点
 * api.getDataPoints(设备id, 参数)
 * 参数为一个json对象，可以设置各个读取参数，参数列表参考http://open.iot.10086.cn/apidoc/datapoint/view.html
 * */
function getDataPos(){
	api.getDataPoints(559451901, {datastream_id:'temperature'}).done(function(data){
	    console.log('api调用完成，服务器返回data为：', data);
		if(data.error === 'succ'){
			var atPoint = data.data.datastreams[0].datapoints[0]["at"];
			var valuePoint = data.data.datastreams[0].datapoints[0]["value"];
			mui.toast(atPoint+" "+valuePoint);
			mui.toast("updated");
		}else{
			mui.toast("Update failed");
		}
	});
 }
 
 
 function getDataStrFromFlask() {
	 var getIP = document.getElementById('path1').value;
    $.ajax({
       type: "GET",
       url: "http://"+getIP+":5000/getSensorsData",
       dataType: "json",
       success : function(data){
     
           $(".temp").empty;
           $(".temp").text(data['temp']);
           
           $(".humi").empty;
           $(".humi").text(data['humi']);
		   
		   
		   $(".gas").empty;
		   if(data['gas'] === 0){
		   				$(".gas").text("closed");
		   }else{
		   				$(".gas").text("triggered");
		   				mui.alert('Gas is triggered. Be careful!','AlarmInfo','got it');
		   }
		   
		   $(".motion").empty;
		   if(data['motion'] === 0){
		   				$(".motion").text("closed");
		   }else{
		   				$(".motion").text("triggered");
		   				mui.alert('Motion is triggered. Be careful!','AlarmInfo','got it');
		   }
		   
		   $(".fire").empty;
		   if(data['fire'] === 0){
		   				$(".fire").text("closed");
		   }else{
		   				$(".fire").text("triggered");
		   				mui.alert('Fire is triggered. Be careful!','AlarmInfo','got it');
		   }
		   
		   $(".soil").empty;
		   if(data['soil'] === 0){
		   				$(".soil").text("closed");
		   }else{
		   				$(".soil").text("triggered");
		   				mui.alert('Soil is triggered. Be careful!','AlarmInfo','got it');
		   }
		   
		   $(".rain").empty;
		   if(data['rain'] === 0){
		   				$(".rain").text("closed");
		   }else{
		   				$(".rain").text("triggered");
		   				mui.alert('Rain is triggered. Be careful!','AlarmInfo','got it');
		   }
		   
		   $(".relay").empty;
		   if(data['relay'] === 0){
		   				$(".relay").text("closed");
		   }else{
		   				$(".relay").text("opened");
		   }
		   
		   $(".motor").empty;
		   if(data['motor'] === 0){
		   				$(".motor").text("closed");
		   }else{
		   				$(".motor").text("opened");
		   }
		   
		   if(data['humi'] > 70)
		   {
				mui.alert('The humidity is too high. Be careful!','AlarmInfo','got it');
		   }
		   
		   if(data['temp'] > 35)
		   {
		   		mui.alert('The temperature is too high. Be careful!','AlarmInfo','got it');
		   }
       }
     });
}
	 
function onRelay(getIP){
		 var data= {
		             data: JSON.stringify({
		                 'relay': 'on'
		             }),
		         }
         $.ajax({
             type:'POST',
             url:"http://"+getIP+":5000/ctl_cmd",
			 data:data,
			 dataType: "json",
             success:function(data){
                 mui.toast("succ!");
             },
             error:function(){
                 mui.toast('failed!')
             }
         });
     }

function offRelay(getIP){
	
		var data= {
	                data: JSON.stringify({
	                    'relay': 'off'
	                }),
	            }
         $.ajax({
             type:'POST',
             url:"http://"+getIP+":5000/ctl_cmd",
			 data:data,
			 dataType: "json",
             success:function(data){
                 mui.toast("succ!");
             },
             error:function(){
                 mui.toast('failed!')
             }
         });
     }

function onMotor(getIP){
		var data= {
		            data: JSON.stringify({
		                'motor': 'on'
		            }),
		        }
         $.ajax({
             type:'POST',
             url:"http://"+getIP+":5000/ctl_cmd",
			 data:data,
			 dataType: "json",
             success:function(data){
                 mui.toast("succ!");
             },
             error:function(){
                 mui.toast('failed!')
             }
         });
     }

function offMotor(getIP){
		var data= {
		            data: JSON.stringify({
		                'motor': 'off'
		            }),
		        }
         $.ajax({
             type:'POST',
             url:"http://"+getIP+":5000/ctl_cmd",
			 data:data,
			 dataType: "json",
             success:function(data){
                 mui.toast("succ!");
             },
             error:function(){
                 mui.toast('failed!')
             }
         });
     }

/**
 * 发送命令
 * api.sendCommand(设备id, 命令内容) 命令内容参考http://open.iot.10086.cn/apidoc/cmd/create.html
 * */
 function sendCom(cmd){
	api.sendCommand(559451901, cmd).done(function(data){
	    console.log('api调用完成，服务器返回data为：', data);
		if(data.error == "succ"){
			mui.toast(data.error);
		}else{
			mui.toast(data.error);	
		}
	});
 }

//接听Update按键是否按下
document.getElementById("update").addEventListener('tap',function(){
	//调用获取数据按钮
	var getIP = document.getElementById('path1').value;
	if(!getIP){
		//远程连接OneNet并获取数据
		mui.toast("To start the update");
		setInterval("getDataStrFromOneNet()", 3000);
	}else{
		//进入Flask
		mui.toast("To start the update");
		setInterval("getDataStrFromFlask()", 3000);
	}
	
})


document.getElementById('btnRelay').addEventListener('toggle', function(event) {
		//event.detail.isActive 可直接获取当前状态
		//this.parentNode.querySelector('span').innerText = '状态：' + (event.detail.isActive ? 'true' : 'false');
		var getIP = document.getElementById('path1').value;
		if(event.detail.isActive){
			if(!getIP){
				//远程连接OneNet并控制
				sendCom('01');//打开继电器
			}else{
				//进入Flask并控制
				onRelay(getIP);
			}
			
		}else{
			if(!getIP){
				//远程连接OneNet并控制
				sendCom('00');//关闭继电器
			}else{
				//进入Flask并控制
				offRelay(getIP);
			}
		}
});

document.getElementById('btnMotor').addEventListener('toggle', function(event) {
		//event.detail.isActive 可直接获取当前状态
		//this.parentNode.querySelector('span').innerText = '状态：' + (event.detail.isActive ? 'true' : 'false');
		var getIP = document.getElementById('path1').value;
		if(event.detail.isActive){
			if(!getIP){
				//远程连接OneNet并控制
				sendCom('11');//打开电机
			}else{
				//进入Flask并控制
				onMotor(getIP);
			}
			
		}else{
			if(!getIP){
				//远程连接OneNet并控制
				sendCom('10');//关闭电机
			}else{
				//进入Flask并控制
				offMotor(getIP);
			}
		}
});