$(function () {

			Chart.defaults.global.defaultFontFamily = "Segoe UI','Arial','Helvetica','sans-serif'";
			
            var ctx = document.getElementById('myChart');
					var mixedChart = new Chart(ctx, {
						type: 'bar',
						data: {
							datasets: [{
								label: '# dataset',
								data: [27, 79, 131, 174, 226, 1762, 2246, 4036, 4484, 4550, 5500, 10500],
								yAxisID: 'y-axis-2',
								order: 1
							}, {
								label: '# visualizzazioni',
								data: [35000, 40000, 98000, 150000, 160000, 200000, 180000, 200000, 210000, 255000, 280000, 340000],
								type: 'line',
								borderColor: [
                                    'rgba(30, 139, 195, 1)'
                                ],
                                borderWidth: 5,
                                fill: false,
                                lineTension: 0,
								order: 2
							}, {
								label: '# download',
								data: [null, null, null, null, null, 99000, 100000, 110000, 270000, 365000, 370000, 405000],
								type: 'line',
								borderColor: [
                                    'rgba(245, 171, 53, 1)'
                                ],
                                borderWidth: 5,
                                fill: false,
                                lineTension: 0,
								order: 3
							}],
							labels: ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
						},
						options: {
							layout: {
								padding: {
									left: 0,
									right: 0,
									top: 0,
									bottom: 0
								}
							},
                            scales: {
								xAxes: [{
                                    ticks: {
										fontSize: 40
                                    }
                                }],
								yAxes: [{
									id: 'y-axis-1',
									type: 'linear', 
                                    ticks: {
										fontSize: 48,
                                        beginAtZero: true
                                    }
                                }
								,
								{
									id: 'y-axis-2',
									type: 'linear', 
									display: true,
									max:5000,
									position: 'right',
                                    ticks: {
										fontSize: 48,
                                        beginAtZero: true
                                    }
                                }
								]
                            }
                        }
					});

});
