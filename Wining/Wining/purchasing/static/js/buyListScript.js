const btnCancel = document.getElementById("btnCancel");
btnCancel.addEventListener("click", cancelPayment);


function cancelPayment(){
	const checkCancel = confirm("결제를 취소하시겠습니까?\n메인 페이지로 이동합니다");
	
	if (checkCancel == true){
		location.href = "store-list"
	}
	else{
		return false
	}
}